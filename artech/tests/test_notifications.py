# Copyright (c) 2015, Artech and Contributors
# MIT License. See license.txt

import artech_engine
from artech_engine.desk import notifications

from artech.tests.utils import ArtechTestSuite


class TestNotifications(ArtechTestSuite):
	def test_get_notifications_for_targets(self):
		"""
		Test notification config entries for targets as percentages
		"""

		company = artech_engine.get_all("Company")[0]
		artech_engine.db.set_value("Company", company.name, "monthly_sales_target", 10000)
		artech_engine.db.set_value("Company", company.name, "total_monthly_sales", 1000)

		config = notifications.get_notification_config()
		doc_target_percents = notifications.get_notifications_for_targets(config, {})

		self.assertEqual(doc_target_percents["Company"][company.name], 10)

		artech_engine.db.set_value("Company", company.name, "monthly_sales_target", 2000)
		artech_engine.db.set_value("Company", company.name, "total_monthly_sales", 0)

		config = notifications.get_notification_config()
		doc_target_percents = notifications.get_notifications_for_targets(config, {})

		self.assertEqual(doc_target_percents["Company"][company.name], 0)
