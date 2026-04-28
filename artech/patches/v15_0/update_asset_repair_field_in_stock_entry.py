import artech_engine
from artech_engine.query_builder import DocType


def execute():
	if artech_engine.db.has_column("Asset Repair", "stock_entry"):
		AssetRepair = DocType("Asset Repair")
		StockEntry = DocType("Stock Entry")

		(
			artech_engine.qb.update(StockEntry)
			.join(AssetRepair)
			.on(StockEntry.name == AssetRepair.stock_entry)
			.set(StockEntry.asset_repair, AssetRepair.name)
		).run()
