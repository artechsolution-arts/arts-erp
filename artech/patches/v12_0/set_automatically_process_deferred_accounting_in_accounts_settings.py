import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "accounts_settings")

	artech_engine.db.set_single_value("Accounts Settings", "automatically_process_deferred_accounting_entry", 1)
