import artech_engine


def execute():
	artech_engine.delete_doc("DocType", "Amazon MWS Settings", ignore_missing=True)
