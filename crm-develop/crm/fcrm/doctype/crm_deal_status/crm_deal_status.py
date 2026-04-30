# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class CRMDealStatus(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		color: DF.Literal[
			"black",
			"gray",
			"blue",
			"green",
			"red",
			"pink",
			"orange",
			"amber",
			"yellow",
			"cyan",
			"teal",
			"violet",
			"purple",
		]
		deal_status: DF.Data
		position: DF.Int
		probability: DF.Percent
		type: DF.Literal["Open", "Ongoing", "On Hold", "Won", "Lost"]
	# end: auto-generated types

	pass
