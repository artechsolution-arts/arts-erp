import artech_engine


def execute():
	artech_engine.delete_doc("DocType", "Woocommerce Settings", ignore_missing=True)
