import artech_engine
from artech_engine.utils.nestedset import rebuild_tree


def execute():
	artech_engine.reload_doc("setup", "doctype", "company")
	rebuild_tree("Company")
