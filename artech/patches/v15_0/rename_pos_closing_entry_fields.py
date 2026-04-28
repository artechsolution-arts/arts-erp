import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	rename_field("POS Closing Entry", "pos_transactions", "pos_invoices", validate=False)
	if artech_engine.db.exists("DocType", "Sales Invoice Reference"):
		rename_field("POS Closing Entry", "sales_invoice_transactions", "sales_invoices", validate=False)
