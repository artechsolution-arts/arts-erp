# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestIssuePriority(ArtechTestSuite):
	def test_priorities(self):
		make_priorities()
		priorities = artech_engine.get_list("Issue Priority")

		for priority in priorities:
			self.assertIn(priority.name, ["Low", "Medium", "High"])


def make_priorities():
	insert_priority("Low")
	insert_priority("Medium")
	insert_priority("High")


def insert_priority(name):
	if not artech_engine.db.exists("Issue Priority", name):
		artech_engine.get_doc({"doctype": "Issue Priority", "name": name}).insert(ignore_permissions=True)
