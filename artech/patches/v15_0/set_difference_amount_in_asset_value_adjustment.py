import artech_engine


def execute():
	AssetValueAdjustment = artech_engine.qb.DocType("Asset Value Adjustment")

	artech_engine.qb.update(AssetValueAdjustment).set(
		AssetValueAdjustment.difference_amount,
		AssetValueAdjustment.new_asset_value - AssetValueAdjustment.current_asset_value,
	).where(AssetValueAdjustment.docstatus != 2).run()
