import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.reload_doc("assets", "doctype", "asset")
	if artech_engine.db.has_column("Asset", "purchase_receipt_amount"):
		rename_field("Asset", "purchase_receipt_amount", "purchase_amount")
