# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class CRMTerritory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_crm_territory: DF.Link | None
		rgt: DF.Int
		territory_manager: DF.Link | None
		territory_name: DF.Data
	# end: auto-generated types

	pass
