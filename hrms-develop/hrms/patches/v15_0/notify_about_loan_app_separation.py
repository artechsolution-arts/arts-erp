import artech_engine
from artech_engine import _
from artech_engine.desk.doctype.notification_log.notification_log import make_notification_logs
from artech_engine.utils.user import get_system_managers


def execute():
	if "lending" in artech_engine.get_installed_apps():
		return

	if artech_engine.db.a_row_exists("Salary Slip Loan"):
		notify_existing_users()


def notify_existing_users():
	subject = _("WARNING: Loan Management module has been separated from ERPNext.") + "<br>"
	subject += _(
		"If you are using loans in salary slips, please install the {0} app from Frappe Cloud Marketplace or GitHub to continue using loan integration with payroll."
	).format(artech_engine.bold("Lending"))

	notification = {
		"subject": subject,
		"type": "Alert",
	}
	make_notification_logs(notification, get_system_managers(only_name=True))
