# For license information, please see license.txt

import copy

import artech_engine
from artech_engine import _, qb
from artech_engine.model.document import Document
from artech_engine.query_builder.custom import ConstantColumn

from artech.accounts.utils import _delete_adv_pl_entries, _delete_pl_entries, create_payment_ledger_entry

VOUCHER_TYPES = ["Sales Invoice", "Purchase Invoice", "Payment Entry", "Journal Entry"]


def repost_ple_for_voucher(voucher_type, voucher_no, gle_map=None):
	if voucher_type and voucher_no and gle_map:
		_delete_pl_entries(voucher_type, voucher_no)
		_delete_adv_pl_entries(voucher_type, voucher_no)
		create_payment_ledger_entry(gle_map, cancel=0)


@artech_engine.whitelist()
def start_payment_ledger_repost(docname: str | None = None):
	"""
	Repost Payment Ledger Entries for Vouchers through Background Job
	"""
	if docname:
		repost_doc = artech_engine.get_doc("Repost Payment Ledger", docname)
		if repost_doc.docstatus.is_submitted() and repost_doc.repost_status in ["Queued", "Failed"]:
			try:
				for entry in repost_doc.repost_vouchers:
					doc = artech_engine.get_doc(entry.voucher_type, entry.voucher_no)

					if doc.doctype in ["Payment Entry", "Journal Entry"]:
						gle_map = doc.build_gl_map()
					else:
						gle_map = doc.get_gl_entries()

					repost_ple_for_voucher(entry.voucher_type, entry.voucher_no, gle_map)

				artech_engine.db.set_value(repost_doc.doctype, repost_doc.name, "repost_error_log", "")
				artech_engine.db.set_value(repost_doc.doctype, repost_doc.name, "repost_status", "Completed")
			except Exception:
				artech_engine.db.rollback()

				traceback = artech_engine.get_traceback(with_context=True)
				if traceback:
					message = "Traceback: <br>" + traceback
					artech_engine.db.set_value(repost_doc.doctype, repost_doc.name, "repost_error_log", message)

				artech_engine.db.set_value(repost_doc.doctype, repost_doc.name, "repost_status", "Failed")


class RepostPaymentLedger(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.accounts.doctype.repost_payment_ledger_items.repost_payment_ledger_items import (
			RepostPaymentLedgerItems,
		)

		add_manually: DF.Check
		amended_from: DF.Link | None
		company: DF.Link
		posting_date: DF.Date
		repost_error_log: DF.LongText | None
		repost_status: DF.Literal["", "Queued", "Failed", "Completed"]
		repost_vouchers: DF.Table[RepostPaymentLedgerItems]
		voucher_type: DF.Link | None
	# end: auto-generated types

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.vouchers = []

	def before_validate(self):
		self.load_vouchers_based_on_filters()
		self.set_status()

	def load_vouchers_based_on_filters(self):
		if not self.add_manually:
			self.repost_vouchers.clear()
			self.get_vouchers()
			self.extend("repost_vouchers", copy.deepcopy(self.vouchers))

	def get_vouchers(self):
		self.vouchers.clear()

		filter_on_voucher_types = [self.voucher_type] if self.voucher_type else VOUCHER_TYPES

		for vtype in filter_on_voucher_types:
			doc = qb.DocType(vtype)
			doctype_name = ConstantColumn(vtype)
			query = (
				qb.from_(doc)
				.select(doctype_name.as_("voucher_type"), doc.name.as_("voucher_no"))
				.where(
					(doc.docstatus == 1)
					& (doc.company == self.company)
					& (doc.posting_date.gte(self.posting_date))
				)
			)
			entries = query.run(as_dict=True)
			self.vouchers.extend(entries)

	def set_status(self):
		if self.docstatus == 0:
			self.repost_status = "Queued"

	def on_submit(self):
		execute_repost_payment_ledger(self.name)
		artech_engine.msgprint(_("Repost started in the background"))


@artech_engine.whitelist()
def execute_repost_payment_ledger(docname: str):
	"""Repost Payment Ledger Entries by background job."""

	job_name = "payment_ledger_repost_" + docname

	artech_engine.enqueue(
		method="artech.accounts.doctype.repost_payment_ledger.repost_payment_ledger.start_payment_ledger_repost",
		docname=docname,
		is_async=True,
		job_name=job_name,
	)
