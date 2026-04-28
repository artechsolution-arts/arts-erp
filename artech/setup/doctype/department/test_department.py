# Copyright (c) 2015, Artech and Contributors

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestDepartment(ArtechTestSuite):
	def test_remove_department_data(self):
		doc = create_department("Test Department", company="_Test Company")
		artech_engine.delete_doc("Department", doc.name)


def create_department(department_name, parent_department=None, company=None):
	doc = artech_engine.get_doc(
		{
			"doctype": "Department",
			"is_group": 0,
			"parent_department": parent_department,
			"department_name": department_name,
			"company": artech_engine.defaults.get_defaults().company or company,
		}
	).insert()

	return doc
