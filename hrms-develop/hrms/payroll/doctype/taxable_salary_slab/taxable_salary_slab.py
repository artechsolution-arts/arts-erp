# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class TaxableSalarySlab(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		condition: DF.Code | None
		from_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percent_deduction: DF.Percent
		to_amount: DF.Currency
	# end: auto-generated types

	pass
