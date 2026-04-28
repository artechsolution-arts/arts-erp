# Copyright (c) 2015, Artech and Contributors and Contributors
# See license.txt

import artech_engine

from artech.projects.doctype.activity_cost.activity_cost import DuplicationError
from artech.tests.utils import ArtechTestSuite


class TestActivityCost(ArtechTestSuite):
	def test_duplication(self):
		employee = artech_engine.db.get_all("Employee", filters={"first_name": "_Test Employee"})[0].name
		activity_type = artech_engine.db.get_all(
			"Activity Type", filters={"activity_type": "_Test Activity Type 1"}
		)[0].name

		activity_cost1 = artech_engine.new_doc("Activity Cost")
		activity_cost1.update(
			{
				"employee": employee,
				"employee_name": employee,
				"activity_type": activity_type,
				"billing_rate": 100,
				"costing_rate": 50,
			}
		)
		activity_cost1.insert()
		activity_cost2 = artech_engine.copy_doc(activity_cost1)
		self.assertRaises(DuplicationError, activity_cost2.insert)
