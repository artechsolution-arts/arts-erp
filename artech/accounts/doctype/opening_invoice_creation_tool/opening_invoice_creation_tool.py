# For license information, please see license.txt


import artech_engine
from artech_engine import _, scrub
from artech_engine.model.document import Document
from artech_engine.utils import escape_html, flt, nowdate
from artech_engine.utils.background_jobs import enqueue, is_job_enqueued

from artech.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from artech.stock.utils import get_default_stock_uom


class OpeningInvoiceCreationTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.accounts.doctype.opening_invoice_creation_tool_item.opening_invoice_creation_tool_item import (
			OpeningInvoiceCreationToolItem,
		)

		company: DF.Link
		cost_center: DF.Link | None
		create_missing_party: DF.Check
		invoice_type: DF.Literal["Sales", "Purchase"]
		invoices: DF.Table[OpeningInvoiceCreationToolItem]
		project: DF.Link | None
	# end: auto-generated types

	def onload(self):
		"""Load the Opening Invoice summary"""
		summary, max_count = self.get_opening_invoice_summary()
		self.set_onload("opening_invoices_summary", summary)
		self.set_onload("max_count", max_count)
		self.set_onload("temporary_opening_account", get_temporary_opening_account(self.company))

	def get_opening_invoice_summary(self):
		def prepare_invoice_summary(doctype, invoices):
			# add company wise sales / purchase invoice summary
			paid_amount = []
			outstanding_amount = []
			for invoice in invoices:
				company = invoice.pop("company")
				_summary = invoices_summary.get(company, {})
				_summary.update({"currency": company_wise_currency.get(company), doctype: invoice})
				invoices_summary.update({company: _summary})

				if invoice.paid_amount:
					paid_amount.append(invoice.paid_amount)
				if invoice.outstanding_amount:
					outstanding_amount.append(invoice.outstanding_amount)

			if paid_amount or outstanding_amount:
				max_count.update(
					{
						doctype: {
							"max_paid": max(paid_amount) if paid_amount else 0.0,
							"max_due": max(outstanding_amount) if outstanding_amount else 0.0,
						}
					}
				)

		invoices_summary = {}
		max_count = {}
		fields = [
			"company",
			{"COUNT": "*", "as": "total_invoices"},
			{"SUM": "outstanding_amount", "as": "outstanding_amount"},
		]
		companies = artech_engine.get_all("Company", fields=["name as company", "default_currency as currency"])
		if not companies:
			return None, None

		company_wise_currency = {row.company: row.currency for row in companies}
		for doctype in ["Sales Invoice", "Purchase Invoice"]:
			invoices = artech_engine.get_all(
				doctype, filters=dict(is_opening="Yes", docstatus=1), fields=fields, group_by="company"
			)
			prepare_invoice_summary(doctype, invoices)

		invoices_summary_companies = list(invoices_summary.keys())

		for company in invoices_summary_companies:
			invoices_summary[escape_html(company)] = invoices_summary.pop(company)

		return invoices_summary, max_count

	def validate_company(self):
		if not self.company:
			artech_engine.throw(_("Please select the Company"))

	def set_missing_values(self, row):
		row.qty = row.qty or 1.0
		row.temporary_opening_account = row.temporary_opening_account or get_temporary_opening_account(
			self.company
		)
		row.party_type = "Customer" if self.invoice_type == "Sales" else "Supplier"
		row.item_name = row.item_name or _("Opening Invoice Item")
		row.posting_date = row.posting_date or nowdate()
		row.due_date = row.due_date or nowdate()

	def validate_mandatory_invoice_fields(self, row):
		if self.create_missing_party:
			if not row.party and not row.party_name:
				artech_engine.throw(_("Row #{}: Either Party ID or Party Name is required").format(row.idx))

			if not row.party and row.party_name:
				row.party = self.add_party(row.party_type, row.party_name)

			if row.party and not artech_engine.db.exists(row.party_type, row.party):
				row.party = self.add_party(row.party_type, row.party)

		else:
			if not row.party:
				artech_engine.throw(_("Row #{}: Party ID is required").format(row.idx))
			if not artech_engine.db.exists(row.party_type, row.party):
				artech_engine.throw(
					_("Row #{}: {} {} does not exist.").format(
						row.idx, artech_engine.bold(row.party_type), artech_engine.bold(row.party)
					)
				)

		mandatory_error_msg = _("Row #{0}: {1} is required to create the Opening {2} Invoices")
		for d in ("Outstanding Amount", "Temporary Opening Account"):
			if not row.get(scrub(d)):
				artech_engine.throw(mandatory_error_msg.format(row.idx, d, self.invoice_type))

	def get_invoices(self):
		invoices = []
		for row in self.invoices:
			if not row:
				continue
			self.set_missing_values(row)
			self.validate_mandatory_invoice_fields(row)
			invoice = self.get_invoice_dict(row)
			company_details = (
				artech_engine.get_cached_value(
					"Company", self.company, ["default_currency", "default_letter_head"], as_dict=1
				)
				or {}
			)

			default_currency = artech_engine.db.get_value(row.party_type, row.party, "default_currency")

			if company_details:
				invoice.update(
					{
						"currency": default_currency or company_details.get("default_currency"),
						"letter_head": company_details.get("default_letter_head"),
					}
				)
			invoices.append(invoice)

		return invoices

	def add_party(self, party_type, party):
		party_doc = artech_engine.new_doc(party_type)
		if party_type == "Customer":
			party_doc.customer_name = party
		else:
			supplier_group = artech_engine.db.get_single_value("Buying Settings", "supplier_group")
			if not supplier_group:
				artech_engine.throw(_("Please Set Supplier Group in Buying Settings."))

			party_doc.supplier_name = party
			party_doc.supplier_group = supplier_group

		party_doc.flags.ignore_mandatory = True
		party_doc.save(ignore_permissions=True)
		return party_doc.name

	def get_invoice_dict(self, row=None):
		def get_item_dict():
			cost_center = row.get("cost_center") or artech_engine.get_cached_value(
				"Company", self.company, "cost_center"
			)
			if not cost_center:
				artech_engine.throw(
					_("Please set the Default Cost Center in {0} company.").format(artech_engine.bold(self.company))
				)

			income_expense_account_field = (
				"income_account" if row.party_type == "Customer" else "expense_account"
			)
			default_uom = get_default_stock_uom()
			rate = flt(row.outstanding_amount) / flt(row.qty)

			item_dict = artech_engine._dict(
				{
					"uom": default_uom,
					"rate": rate or 0.0,
					"qty": row.qty,
					"conversion_factor": 1.0,
					"item_name": row.item_name or "Opening Invoice Item",
					"description": row.item_name or "Opening Invoice Item",
					income_expense_account_field: row.temporary_opening_account,
					"cost_center": cost_center,
				}
			)

			for dimension in get_accounting_dimensions():
				item_dict.update({dimension: row.get(dimension)})

			return item_dict

		item = get_item_dict()

		invoice = artech_engine._dict(
			{
				"items": [item],
				"is_opening": "Yes",
				"set_posting_time": 1,
				"company": self.company,
				"cost_center": self.cost_center,
				"due_date": row.due_date,
				"posting_date": row.posting_date,
				artech_engine.scrub(row.party_type): row.party,
				"is_pos": 0,
				"doctype": "Sales Invoice" if self.invoice_type == "Sales" else "Purchase Invoice",
				"update_stock": 0,  # important: https://github.com/artech_engine/artech/pull/23559
				"invoice_number": row.invoice_number,
				"disable_rounded_total": 1,
			}
		)

		if self.invoice_type == "Purchase" and row.supplier_invoice_date:
			invoice.update({"bill_date": row.supplier_invoice_date})

		accounting_dimension = get_accounting_dimensions()
		for dimension in accounting_dimension:
			invoice.update({dimension: self.get(dimension) or item.get(dimension)})

		return invoice

	@artech_engine.whitelist()
	def make_invoices(self):
		self.validate_company()
		invoices = self.get_invoices()
		if len(invoices) < 50:
			return start_import(invoices)
		else:
			from artech_engine.utils.scheduler import is_scheduler_inactive

			if is_scheduler_inactive() and not artech_engine.in_test:
				artech_engine.throw(_("Scheduler is inactive. Cannot import data."), title=_("Scheduler Inactive"))

			job_id = f"opening_invoice::{self.name}"

			if not is_job_enqueued(job_id):
				enqueue(
					start_import,
					queue="default",
					timeout=6000,
					event="opening_invoice_creation",
					job_id=job_id,
					invoices=invoices,
					now=artech_engine.conf.developer_mode or artech_engine.in_test,
				)


def start_import(invoices):
	errors = 0
	names = []
	for idx, d in enumerate(invoices):
		try:
			invoice_number = None
			if d.invoice_number:
				invoice_number = d.invoice_number
			publish(idx, len(invoices), d.doctype)
			doc = artech_engine.get_doc(d)
			doc.flags.ignore_mandatory = True
			doc.insert(set_name=invoice_number)
			doc.submit()
			if not artech_engine.in_test:
				artech_engine.db.commit()
			names.append(doc.name)
		except Exception:
			errors += 1
			artech_engine.db.rollback()
			doc.log_error("Opening invoice creation failed")
	if errors:
		artech_engine.msgprint(
			_("You had {} errors while creating opening invoices. Check {} for more details").format(
				errors, "<a href='/app/List/Error Log' class='variant-click'>Error Log</a>"
			),
			indicator="red",
			title=_("Error Occurred"),
		)
	return names


def publish(index, total, doctype):
	artech_engine.publish_realtime(
		"opening_invoice_creation_progress",
		dict(
			title=_("Opening Invoice Creation In Progress"),
			message=_("Creating {} out of {} {}").format(index + 1, total, doctype),
			count=index + 1,
			total=total,
		),
		user=artech_engine.session.user,
	)


@artech_engine.whitelist()
def get_temporary_opening_account(company: str | None = None):
	if not company:
		return

	accounts = artech_engine.get_all("Account", filters={"company": company, "account_type": "Temporary"})
	if not accounts:
		artech_engine.throw(_("Please add a Temporary Opening account in Chart of Accounts"))

	return accounts[0].name
