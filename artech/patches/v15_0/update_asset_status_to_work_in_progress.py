import artech_engine


def execute():
	Asset = artech_engine.qb.DocType("Asset")
	query = (
		artech_engine.qb.update(Asset)
		.set(Asset.status, "Work In Progress")
		.where((Asset.docstatus == 0) & (Asset.is_composite_asset == 1))
	)
	query.run()
