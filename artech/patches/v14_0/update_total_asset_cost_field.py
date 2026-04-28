import artech_engine


def execute():
	asset = artech_engine.qb.DocType("Asset")
	artech_engine.qb.update(asset).set(asset.total_asset_cost, asset.net_purchase_amount).run()

	asset_repair_list = artech_engine.db.get_all(
		"Asset Repair",
		filters={"docstatus": 1, "repair_status": "Completed", "capitalize_repair_cost": 1},
		fields=["asset", "repair_cost"],
	)

	for asset_repair in asset_repair_list:
		artech_engine.qb.update(asset).set(
			asset.total_asset_cost, asset.total_asset_cost + asset_repair.repair_cost
		).where(asset.name == asset_repair.asset).run()
