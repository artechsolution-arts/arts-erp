import artech_engine


def execute():
	doctypes = artech_engine.get_all("DocType", {"module": "Hub Node", "custom": 0}, pluck="name")
	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True)

	artech_engine.delete_doc("Module Def", "Hub Node", ignore_missing=True, force=True)
