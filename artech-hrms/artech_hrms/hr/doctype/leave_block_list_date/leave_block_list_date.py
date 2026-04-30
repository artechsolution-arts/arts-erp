# For license information, please see license.txt


from artech_engine.model.document import Document


class LeaveBlockListDate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		block_date: DF.Date
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reason: DF.Text
	# end: auto-generated types

	pass
