import artech_engine


def execute():
	if artech_engine.db.exists("Page", "point-of-sale"):
		artech_engine.rename_doc("Page", "pos", "point-of-sale", 1, 1)
