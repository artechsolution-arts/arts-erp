# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class ItemWiseTaxDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amount: DF.Currency
		item_row: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		rate: DF.Float
		tax_row: DF.Data
		taxable_amount: DF.Currency
	# end: auto-generated types

	pass
