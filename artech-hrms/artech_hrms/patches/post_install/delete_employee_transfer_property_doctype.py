import artech_engine


def execute():
	artech_engine.delete_doc("DocType", "Employee Transfer Property", ignore_missing=True)
