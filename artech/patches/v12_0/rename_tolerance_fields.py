import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.reload_doc("stock", "doctype", "item")
	artech_engine.reload_doc("stock", "doctype", "stock_settings")
	artech_engine.reload_doc("accounts", "doctype", "accounts_settings")

	rename_field("Stock Settings", "tolerance", "over_delivery_receipt_allowance")
	rename_field("Item", "tolerance", "over_delivery_receipt_allowance")

	qty_allowance = artech_engine.db.get_single_value("Stock Settings", "over_delivery_receipt_allowance")
	artech_engine.db.set_single_value("Accounts Settings", "over_delivery_receipt_allowance", qty_allowance)

	artech_engine.db.sql("update tabItem set over_billing_allowance=over_delivery_receipt_allowance")
