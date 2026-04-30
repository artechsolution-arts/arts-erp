# For license information, please see license.txt


from artech_engine.model.document import Document


class JobOfferTerm(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		offer_term: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		value: DF.SmallText
	# end: auto-generated types

	pass
