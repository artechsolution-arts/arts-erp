import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "bank", force=1)

	if (
		artech_engine.db.table_exists("Bank")
		and artech_engine.db.table_exists("Bank Account")
		and artech_engine.db.has_column("Bank Account", "swift_number")
	):
		try:
			artech_engine.db.sql(
				"""
				UPDATE `tabBank` b, `tabBank Account` ba
				SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
			"""
			)
		except Exception:
			artech_engine.log_error("Bank to Bank Account patch migration failed")

	artech_engine.reload_doc("accounts", "doctype", "bank_account")
	artech_engine.reload_doc("accounts", "doctype", "payment_request")
