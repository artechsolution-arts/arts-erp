import artech_engine


def execute():
	artech_engine.delete_doc("DocType", "Shopify Settings", ignore_missing=True)
	artech_engine.delete_doc("DocType", "Shopify Log", ignore_missing=True)
