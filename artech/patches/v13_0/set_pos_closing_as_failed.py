import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "pos_closing_entry")

	artech_engine.db.sql("update `tabPOS Closing Entry` set `status` = 'Failed' where `status` = 'Queued'")
