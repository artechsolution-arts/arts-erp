# For license information, please see license.txt


from artech_engine.model.document import Document


class IssueType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		description: DF.SmallText | None
	# end: auto-generated types

	pass
