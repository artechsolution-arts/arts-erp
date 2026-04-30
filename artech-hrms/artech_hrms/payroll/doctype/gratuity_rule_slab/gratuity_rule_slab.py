# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class GratuityRuleSlab(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		fraction_of_applicable_earnings: DF.Float
		from_year: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		to_year: DF.Int
	# end: auto-generated types

	pass
