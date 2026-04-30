# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class CRMDropdownItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		hidden: DF.Check
		icon: DF.Code | None
		is_standard: DF.Check
		label: DF.Data | None
		name1: DF.Data | None
		open_in_new_window: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		route: DF.Data | None
		type: DF.Literal["Route", "Separator"]
	# end: auto-generated types

	pass
