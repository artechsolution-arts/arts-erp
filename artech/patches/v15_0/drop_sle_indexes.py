import click
import artech_engine


def execute():
	table = "tabStock Ledger Entry"
	index_list = ["posting_datetime_creation_index", "item_warehouse", "batch_no_item_code_warehouse_index"]

	for index in index_list:
		if not artech_engine.db.has_index(table, index):
			continue

		try:
			artech_engine.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
			click.echo(f"✓ dropped {index} index from {table}")
		except Exception:
			artech_engine.log_error("Failed to drop index")
