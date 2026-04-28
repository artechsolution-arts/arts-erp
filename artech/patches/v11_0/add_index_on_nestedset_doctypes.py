# Copyright (c) 2015, Artech and Contributors


import artech_engine


def execute():
	artech_engine.reload_doc("assets", "doctype", "Location")
	for dt in (
		"Account",
		"Cost Center",
		"File",
		"Employee",
		"Location",
		"Task",
		"Customer Group",
		"Sales Person",
		"Territory",
	):
		artech_engine.reload_doctype(dt)
		artech_engine.get_doc("DocType", dt).run_module_method("on_doctype_update")
