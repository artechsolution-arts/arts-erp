# For license information, please see license.txt


from artech_engine.model.document import Document


class TravelRequestCosting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		comments: DF.SmallText | None
		expense_type: DF.Link | None
		funded_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		sponsored_amount: DF.Currency
		total_amount: DF.Currency
	# end: auto-generated types

	pass
