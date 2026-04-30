# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class ExpenseTaxesandCharges(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		account_head: DF.Link
		base_tax_amount: DF.Currency
		base_total: DF.Currency
		cost_center: DF.Link | None
		description: DF.SmallText
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project: DF.Link | None
		rate: DF.Float
		tax_amount: DF.Currency
		total: DF.Currency
	# end: auto-generated types

	pass
