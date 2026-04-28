import artech_engine


def execute():
	for dt in ("GoCardless Settings", "GoCardless Mandate", "Mpesa Settings"):
		artech_engine.delete_doc("DocType", dt, ignore_missing=True)
