# Copyright (c) 2018, Artech and Contributors
# See license.txt

import artech_engine

from artech.setup.doctype.employee.test_employee import make_employee
from artech.tests.utils import ArtechTestSuite


class TestEmployeeGroup(ArtechTestSuite):
	pass


def make_employee_group():
	employee = make_employee("testemployee@example.com")
	employee_group = artech_engine.get_doc(
		{
			"doctype": "Employee Group",
			"employee_group_name": "_Test Employee Group",
			"employee_list": [{"employee": employee}],
		}
	)
	employee_group_exist = artech_engine.db.exists("Employee Group", "_Test Employee Group")
	if not employee_group_exist:
		employee_group.insert()
		return employee_group.employee_group_name
	else:
		return employee_group_exist


def get_employee_group():
	employee_group = artech_engine.db.exists("Employee Group", "_Test Employee Group")
	return employee_group
