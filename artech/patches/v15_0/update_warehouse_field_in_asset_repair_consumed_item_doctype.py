import artech_engine


# not able to use artech_engine.qb because of this bug https://github.com/artech_engine/artech_engine/issues/20292
def execute():
	if artech_engine.db.has_column("Asset Repair", "warehouse"):
		# nosemgrep
		artech_engine.db.sql(
			"""UPDATE `tabAsset Repair Consumed Item` ar_item
			JOIN `tabAsset Repair` ar
			ON ar.name = ar_item.parent
			SET ar_item.warehouse = ar.warehouse
			WHERE ifnull(ar.warehouse, '') != ''"""
		)
