import artech_engine


def execute():
	if artech_engine.db.count("Asset"):
		artech_engine.reload_doc("assets", "doctype", "Asset")
		asset = artech_engine.qb.DocType("Asset")
		artech_engine.qb.update(asset).set(asset.asset_quantity, 1).run()
