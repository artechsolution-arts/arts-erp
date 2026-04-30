import artech_engine
from artech_engine.boot import load_translations

no_cache = 1


def get_context(context):
	csrf_token = artech_engine.sessions.get_csrf_token()
	artech_engine.db.commit()  # nosempgrep
	context = artech_engine._dict()
	context.csrf_token = csrf_token
	context.boot = get_boot()
	context.site_name = artech_engine.local.site
	return context


@artech_engine.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
	if not artech_engine.conf.developer_mode:
		artech_engine.throw(artech_engine._("This method is only meant for developer mode"))
	return get_boot()


def get_boot():
	bootinfo = artech_engine._dict(
		{
			"site_name": artech_engine.local.site,
			"push_relay_server_url": artech_engine.conf.get("push_relay_server_url") or "",
			"default_route": get_default_route(),
		}
	)

	bootinfo.lang = artech_engine.local.lang
	load_translations(bootinfo)

	return bootinfo


def get_default_route():
	return "/artech_hrms"
