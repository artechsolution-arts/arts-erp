# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class EmployeeSkillMap(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.hr.doctype.employee_skill.employee_skill import EmployeeSkill
		from artech_hrms.hr.doctype.employee_training.employee_training import EmployeeTraining

		designation: DF.ReadOnly | None
		employee: DF.Link | None
		employee_name: DF.ReadOnly | None
		employee_skills: DF.Table[EmployeeSkill]
		trainings: DF.Table[EmployeeTraining]
	# end: auto-generated types

	pass
