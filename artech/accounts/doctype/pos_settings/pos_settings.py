# For license information, please see license.txt

from collections import Counter

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class POSSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.accounts.doctype.pos_field.pos_field import POSField
		from artech.accounts.doctype.pos_search_fields.pos_search_fields import POSSearchFields

		invoice_fields: DF.Table[POSField]
		invoice_type: DF.Literal["Sales Invoice", "POS Invoice"]
		pos_search_fields: DF.Table[POSSearchFields]
		post_change_gl_entries: DF.Check
	# end: auto-generated types

	def validate(self):
		old_doc = self.get_doc_before_save()

		if old_doc.invoice_type != self.invoice_type:
			self.validate_invoice_type()

		self.validate_invoice_fields()

	def validate_invoice_fields(self):
		invoice_fields = [field.fieldname for field in self.invoice_fields]
		duplicate_invoice_fields = {key for key, value in Counter(invoice_fields).items() if value > 1}

		if len(duplicate_invoice_fields):
			for field in duplicate_invoice_fields:
				artech_engine.throw(
					title=_("Duplicate POS Fields"), msg=_("'{0}' has been already added.").format(field)
				)

	def validate_invoice_type(self):
		pos_opening_entries_count = artech_engine.db.count(
			"POS Opening Entry", filters={"docstatus": 1, "status": "Open"}
		)
		if pos_opening_entries_count:
			artech_engine.throw(
				_("{0} cannot be changed with opened Opening Entries.").format(
					artech_engine.bold(_("Invoice Type"))
				),
				title=_("Invoice Document Type Selection Error"),
			)
