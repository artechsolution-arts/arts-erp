import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	if artech_engine.db.table_exists("Purchase Order Item") and artech_engine.db.has_column(
		"Purchase Order Item", "sco_qty"
	):
		rename_field("Purchase Order Item", "sco_qty", "subcontracted_quantity")

	if artech_engine.db.table_exists("Subcontracting Order Item") and artech_engine.db.has_column(
		"Subcontracting Order Item", "sc_conversion_factor"
	):
		rename_field("Subcontracting Order Item", "sc_conversion_factor", "subcontracting_conversion_factor")
