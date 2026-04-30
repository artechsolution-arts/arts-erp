# See license.txt

import artech_engine
from artech_engine.utils import getdate

from artech_hrms.tests.utils import HRMSTestSuite


class TestEmployeeSeparation(HRMSTestSuite):
	def test_employee_separation(self):
		separation = create_employee_separation()

		self.assertEqual(separation.docstatus, 1)
		self.assertEqual(separation.boarding_status, "Pending")

		project = artech_engine.get_doc("Project", separation.project)
		project.percent_complete_method = "Manual"
		project.status = "Completed"
		project.save()

		separation.reload()
		self.assertEqual(separation.boarding_status, "Completed")

		separation.cancel()
		self.assertEqual(separation.project, "")


def create_employee_separation():
	employee = artech_engine.db.get_value("Employee", {"status": "Active", "company": "_Test Company"})
	separation = artech_engine.new_doc("Employee Separation")
	separation.employee = employee
	separation.boarding_begins_on = getdate()
	separation.company = "_Test Company"
	separation.append("activities", {"activity_name": "Deactivate Employee", "role": "HR User"})
	separation.boarding_status = "Pending"
	separation.insert()
	separation.submit()
	return separation
