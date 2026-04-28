import artech_engine

from artech.stock.doctype.stock_ledger_entry.stock_ledger_entry import on_doctype_update


def execute():
	try:
		artech_engine.db.sql_ddl("ALTER TABLE `tabStock Ledger Entry` DROP INDEX `posting_sort_index`")
	except Exception:
		artech_engine.log_error("Failed to drop index")
		return

	# Recreate indexes
	on_doctype_update()
