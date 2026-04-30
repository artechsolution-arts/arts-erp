import artech_engine

from artech_hrms.setup import add_lending_docperms_to_ess


def execute():
	if "lending" in artech_engine.get_installed_apps():
		add_lending_docperms_to_ess()
