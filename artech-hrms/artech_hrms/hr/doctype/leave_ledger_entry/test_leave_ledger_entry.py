# See license.txt

import artech_engine
from artech_engine.utils.data import add_to_date, today

from artech.setup.doctype.employee.test_employee import make_employee

from artech_hrms.hr.doctype.leave_ledger_entry.leave_ledger_entry import expire_allocation
from artech_hrms.tests.utils import HRMSTestSuite


class TestLeaveLedgerEntry(HRMSTestSuite):
	def setUp(self):
		emp_id = make_employee("test_leave_allocation@salary.com", company="_Test Company")
		self.employee = artech_engine.get_doc("Employee", emp_id)

	def test_expire_allocation(self):
		import json

		allocation = {
			"doctype": "Leave Allocation",
			"__islocal": 1,
			"employee": self.employee.name,
			"employee_name": self.employee.employee_name,
			"leave_type": "_Test Leave Type",
			"from_date": today(),
			"to_date": add_to_date(today(), days=30),
			"new_leaves_allocated": 5,
			"docstatus": 1,
		}

		allocation = artech_engine.get_doc(allocation).save()

		expire_allocation(json.dumps(allocation.as_dict()))
		allocation.reload()

		self.assertEqual(allocation.expired, 1)
