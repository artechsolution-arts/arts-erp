import artech_engine


def execute():
	install_apps = artech_engine.get_installed_apps()
	if "artech_datev_uo" in install_apps or "artech_datev" in install_apps:
		return

	# doctypes
	artech_engine.delete_doc("DocType", "DATEV Settings", ignore_missing=True, force=True)

	# reports
	artech_engine.delete_doc("Report", "DATEV", ignore_missing=True, force=True)
