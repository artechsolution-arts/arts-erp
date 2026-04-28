import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "bank_account")
	artech_engine.reload_doc("accounts", "doctype", "bank")

	if artech_engine.db.has_column("Bank", "branch_code") and artech_engine.db.has_column("Bank Account", "branch_code"):
		artech_engine.db.sql(
			"""UPDATE `tabBank` b, `tabBank Account` ba
			SET ba.branch_code = b.branch_code
			WHERE ba.bank = b.name AND
			ifnull(b.branch_code, '') != '' AND ifnull(ba.branch_code, '') = ''"""
		)
