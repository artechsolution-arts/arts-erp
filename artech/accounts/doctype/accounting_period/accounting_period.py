# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class OverlapError(artech_engine.ValidationError):
	pass


class ClosedAccountingPeriod(artech_engine.ValidationError):
	pass


class AccountingPeriod(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.accounts.doctype.closed_document.closed_document import ClosedDocument

		closed_documents: DF.Table[ClosedDocument]
		company: DF.Link
		disabled: DF.Check
		end_date: DF.Date
		exempted_role: DF.Link | None
		period_name: DF.Data
		start_date: DF.Date
	# end: auto-generated types

	def validate(self):
		self.validate_overlap()

	def before_insert(self):
		self.bootstrap_doctypes_for_closing()

	def autoname(self):
		company_abbr = artech_engine.get_cached_value("Company", self.company, "abbr")
		self.name = " - ".join([self.period_name, company_abbr])

	def validate_overlap(self):
		existing_accounting_period = artech_engine.db.sql(
			"""select name from `tabAccounting Period`
			where (
				(%(start_date)s between start_date and end_date)
				or (%(end_date)s between start_date and end_date)
				or (start_date between %(start_date)s and %(end_date)s)
				or (end_date between %(start_date)s and %(end_date)s)
			) and name!=%(name)s and company=%(company)s""",
			{
				"start_date": self.start_date,
				"end_date": self.end_date,
				"name": self.name,
				"company": self.company,
			},
			as_dict=True,
		)

		if len(existing_accounting_period) > 0:
			artech_engine.throw(
				_("Accounting Period overlaps with {0}").format(existing_accounting_period[0].get("name")),
				OverlapError,
			)

	@artech_engine.whitelist()
	def get_doctypes_for_closing(self):
		docs_for_closing = []
		# get period closing doctypes from all the apps
		doctypes = artech_engine.get_hooks("period_closing_doctypes")

		closed_doctypes = [{"document_type": doctype, "closed": 1} for doctype in doctypes]
		for closed_doctype in closed_doctypes:
			docs_for_closing.append(closed_doctype)

		return docs_for_closing

	def bootstrap_doctypes_for_closing(self):
		if len(self.closed_documents) == 0:
			for doctype_for_closing in self.get_doctypes_for_closing():
				self.append(
					"closed_documents",
					{
						"document_type": doctype_for_closing.document_type,
						"closed": doctype_for_closing.closed,
					},
				)


def validate_accounting_period_on_doc_save(doc, method=None):
	if doc.doctype == "Bank Clearance":
		return
	elif doc.doctype == "Asset":
		if doc.asset_type == "Existing Asset":
			return
		else:
			date = doc.available_for_use_date
	elif doc.doctype == "Asset Repair":
		date = doc.completion_date
	elif doc.doctype == "Period Closing Voucher":
		date = doc.period_end_date
	else:
		date = doc.posting_date

	ap = artech_engine.qb.DocType("Accounting Period")
	cd = artech_engine.qb.DocType("Closed Document")

	accounting_period = (
		artech_engine.qb.from_(ap)
		.from_(cd)
		.select(ap.name, ap.exempted_role)
		.where(
			(ap.name == cd.parent)
			& (ap.company == doc.company)
			& (ap.disabled == 0)
			& (cd.closed == 1)
			& (cd.document_type == doc.doctype)
			& (date >= ap.start_date)
			& (date <= ap.end_date)
		)
	).run(as_dict=1)

	if accounting_period:
		if (
			accounting_period[0].get("exempted_role")
			and accounting_period[0].get("exempted_role") in artech_engine.get_roles()
		):
			return
		artech_engine.throw(
			_("You cannot create a {0} within the closed Accounting Period {1}").format(
				doc.doctype, artech_engine.bold(accounting_period[0]["name"])
			),
			ClosedAccountingPeriod,
		)
