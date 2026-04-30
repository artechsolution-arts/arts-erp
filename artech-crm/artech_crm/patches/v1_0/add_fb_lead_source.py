import artech_engine


def execute():
	artech_engine.get_doc({"doctype": "CRM Lead Source", "source_name": "Facebook"}).insert(ignore_if_duplicate=True)
