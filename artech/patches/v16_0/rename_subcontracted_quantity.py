import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	if artech_engine.db.has_column("Purchase Order Item", "subcontracted_quantity"):
		rename_field("Purchase Order Item", "subcontracted_quantity", "subcontracted_qty")
