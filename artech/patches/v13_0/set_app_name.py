import artech_engine


def execute():
	artech_engine.reload_doctype("System Settings")
	settings = artech_engine.get_doc("System Settings")
	settings.db_set("app_name", "Artech", commit=True)
