# See license.txt

import artech_engine

from artech.stock.doctype.repost_item_valuation.repost_item_valuation import get_recipients
from artech.tests.utils import ArtechTestSuite


class TestStockRepostingSettings(ArtechTestSuite):
	def test_notify_reposting_error_to_role(self):
		role = "Notify Reposting Role"

		if not artech_engine.db.exists("Role", role):
			artech_engine.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)

		user = "notify_reposting_error@test.com"
		if not artech_engine.db.exists("User", user):
			artech_engine.get_doc(
				{
					"doctype": "User",
					"email": user,
					"first_name": "Test",
					"language": "en",
					"time_zone": "Asia/Kolkata",
					"send_welcome_email": 0,
					"roles": [{"role": role}],
				}
			).insert(ignore_permissions=True)

		artech_engine.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", "")

		users = get_recipients()
		self.assertFalse(user in users)

		artech_engine.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", role)

		users = get_recipients()
		self.assertTrue(user in users)
