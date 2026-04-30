# For license information, please see license.txt


from artech_engine.model.document import Document


class EmployeeOnboardingTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.hr.doctype.employee_boarding_activity.employee_boarding_activity import (
			EmployeeBoardingActivity,
		)

		activities: DF.Table[EmployeeBoardingActivity]
		company: DF.Link | None
		department: DF.Link | None
		designation: DF.Link | None
		employee_grade: DF.Link | None
		title: DF.Data
	# end: auto-generated types

	pass
