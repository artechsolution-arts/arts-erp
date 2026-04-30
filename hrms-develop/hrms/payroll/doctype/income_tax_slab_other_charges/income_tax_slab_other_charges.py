# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class IncomeTaxSlabOtherCharges(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		description: DF.Data
		max_taxable_income: DF.Currency
		min_taxable_income: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percent: DF.Percent
	# end: auto-generated types

	pass
