# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class JournalEntryTemplateAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		account: DF.Link
		cost_center: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		party: DF.DynamicLink | None
		party_type: DF.Link | None
		project: DF.Link | None
	# end: auto-generated types

	pass
