import artech_engine
from artech_engine.query_builder import Case


def execute():
	Asset = artech_engine.qb.DocType("Asset")

	artech_engine.qb.update(Asset).set(
		Asset.asset_type,
		Case()
		.when(Asset.is_existing_asset == 1, "Existing Asset")
		.when(Asset.is_composite_asset == 1, "Composite Asset")
		.when(Asset.is_composite_component == 1, "Composite Component")
		.else_(""),
	).run()
