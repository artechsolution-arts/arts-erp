# GNU GPLv3 License. See license.txt

import artech_engine
from artech_engine import _
from artech_engine.integrations.frappe_providers.frappecloud_billing import is_fc_site
from artech_engine.translate import get_messages_for_boot, get_translated_doctypes
from artech_engine.utils import cint, get_system_timezone
from artech_engine.utils.telemetry import capture

no_cache = 1


def get_context():
	from artech_crm.api import check_app_permission

	if not check_app_permission():
		artech_engine.throw(_("You do not have permission to access Frappe CRM"), artech_engine.PermissionError)

	artech_engine.db.commit()
	context = artech_engine._dict()
	context.boot = get_boot()
	if artech_engine.session.user != "Guest":
		capture("active_site", "artech_crm")
	return context


@artech_engine.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
	if not artech_engine.conf.developer_mode:
		artech_engine.throw(_("This method is only meant for developer mode"))
	return get_boot()


def get_boot():
	return artech_engine._dict(
		{
			"frappe_version": artech_engine.__version__,
			"default_route": get_default_route(),
			"site_name": artech_engine.local.site,
			"read_only_mode": artech_engine.flags.read_only,
			"csrf_token": artech_engine.sessions.get_csrf_token(),
			"setup_complete": cint(artech_engine.get_system_settings("setup_complete")),
			"sysdefaults": artech_engine.defaults.get_defaults(),
			"is_demo_site": artech_engine.conf.get("is_demo_site"),
			"demo_data_created": artech_engine.db.get_default("crm_demo_data_created") == "1",
			"is_fc_site": is_fc_site(),
			"translated_doctypes": get_translated_doctypes(),
			"translated_messages": get_messages_for_boot(),
			"timezone": {
				"system": get_system_timezone(),
				"user": artech_engine.db.get_value("User", artech_engine.session.user, "time_zone")
				or get_system_timezone(),
			},
		}
	)


def get_default_route():
	return "/artech_crm"
