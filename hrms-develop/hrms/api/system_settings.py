import artech_engine


@artech_engine.whitelist(allow_guest=True)
def get_user_pass_login_disabled():
	return artech_engine.get_system_settings("disable_user_pass_login")
