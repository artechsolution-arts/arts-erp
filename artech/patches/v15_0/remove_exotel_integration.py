import click
import artech_engine
from artech_engine import _
from artech_engine.desk.doctype.notification_log.notification_log import make_notification_logs
from artech_engine.utils.user import get_system_managers

SETTINGS_DOCTYPE = "Exotel Settings"


def execute():
	if "exotel_integration" in artech_engine.get_installed_apps():
		return

	try:
		exotel = artech_engine.get_doc(SETTINGS_DOCTYPE)
		if exotel.enabled:
			notify_existing_users()

		artech_engine.delete_doc("DocType", SETTINGS_DOCTYPE)
	except Exception:
		artech_engine.log_error("Failed to remove Exotel Integration.")


def notify_existing_users():
	click.secho(
		"Exotel integration is moved to a separate app and will be removed from Artech in version-15.\n"
		"Please install the app to continue using the integration: https://github.com/artech_engine/exotel_integration",
		fg="yellow",
	)

	notification = {
		"subject": _(
			"WARNING: Exotel app has been separated from Artech, please install the app to continue using Exotel integration."
		),
		"type": "Alert",
	}
	make_notification_logs(notification, get_system_managers(only_name=True))
