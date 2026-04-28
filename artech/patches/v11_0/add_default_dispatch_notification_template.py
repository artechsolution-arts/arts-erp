import os

import artech_engine
from artech_engine import _


def execute():
	artech_engine.reload_doc("email", "doctype", "email_template")
	artech_engine.reload_doc("stock", "doctype", "delivery_settings")

	if not artech_engine.db.exists("Email Template", _("Dispatch Notification")):
		base_path = artech_engine.get_app_path("artech", "stock", "doctype")
		response = artech_engine.read_file(
			os.path.join(base_path, "delivery_trip/dispatch_notification_template.html")
		)

		artech_engine.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Dispatch Notification"),
				"response": response,
				"subject": _("Your order is out for delivery!"),
				"owner": artech_engine.session.user,
			}
		).insert(ignore_permissions=True)

	delivery_settings = artech_engine.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.flags.ignore_links = True
	delivery_settings.save()
