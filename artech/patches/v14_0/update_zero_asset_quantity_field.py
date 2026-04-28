import artech_engine


def execute():
	asset = artech_engine.qb.DocType("Asset")
	artech_engine.qb.update(asset).set(asset.asset_quantity, 1).where(asset.asset_quantity == 0).run()
