import click
import artech_engine


def execute():
	table = "tabStock Ledger Entry"
	index = "posting_datetime_creation_index"

	if not artech_engine.db.has_index(table, index):
		return

	try:
		artech_engine.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
		click.echo(f"✓ dropped {index} index from {table}")
	except Exception:
		artech_engine.log_error("Failed to drop index")
