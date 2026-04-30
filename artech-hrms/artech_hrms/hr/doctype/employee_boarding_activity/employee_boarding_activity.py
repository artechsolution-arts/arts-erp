# For license information, please see license.txt


from artech_engine.model.document import Document


class EmployeeBoardingActivity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		activity_name: DF.Data
		begin_on: DF.Int
		description: DF.TextEditor | None
		duration: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		required_for_employee_creation: DF.Check
		role: DF.Link | None
		task: DF.Link | None
		task_weight: DF.Float
		user: DF.Link | None
	# end: auto-generated types

	pass
