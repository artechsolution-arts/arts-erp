import artech_engine


def execute():
	artech_engine.qb.update("Item Barcode").set("barcode_type", "EAN-13").where(
		artech_engine.qb.Field("barcode_type") == "EAN-12"
	).run()
