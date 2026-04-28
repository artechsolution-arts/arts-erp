import click
import artech_engine

UNUSED_INDEXES = [
	("Delivery Note", ["customer", "is_return", "return_against"]),
	("Sales Invoice", ["customer", "is_return", "return_against"]),
	("Purchase Invoice", ["supplier", "is_return", "return_against"]),
	("Purchase Receipt", ["supplier", "is_return", "return_against"]),
]


def execute():
	for doctype, index_fields in UNUSED_INDEXES:
		table = f"tab{doctype}"
		index_name = artech_engine.db.get_index_name(index_fields)
		drop_index_if_exists(table, index_name)


def drop_index_if_exists(table: str, index: str):
	if not artech_engine.db.has_index(table, index):
		return

	try:
		artech_engine.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
		click.echo(f"✓ dropped {index} index from {table}")
	except Exception:
		artech_engine.log_error("Failed to drop index")
