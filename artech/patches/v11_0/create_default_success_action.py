import artech_engine

from artech.setup.install import create_default_success_action


def execute():
	artech_engine.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
