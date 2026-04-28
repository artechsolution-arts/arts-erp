import artech_engine


def execute():
	artech_engine.rename_doc("DocType", "Account Type", "Bank Account Type", force=True)
	artech_engine.rename_doc("DocType", "Account Subtype", "Bank Account Subtype", force=True)
	artech_engine.reload_doc("accounts", "doctype", "bank_account")
