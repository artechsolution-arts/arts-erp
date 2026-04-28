# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class UnreconcilePaymentEntries(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		account: DF.Data | None
		account_currency: DF.Link | None
		allocated_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		party: DF.Data | None
		party_type: DF.Data | None
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		unlinked: DF.Check
	# end: auto-generated types

	pass
