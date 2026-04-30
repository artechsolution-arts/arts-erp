# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class EmployeeCostCenter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		cost_center: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percentage: DF.Int
	# end: auto-generated types

	pass
