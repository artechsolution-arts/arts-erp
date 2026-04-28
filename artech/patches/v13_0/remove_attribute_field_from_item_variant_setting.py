import artech_engine


def execute():
	"""Remove has_variants and attribute fields from item variant settings."""
	artech_engine.reload_doc("stock", "doctype", "Item Variant Settings")

	artech_engine.db.sql(
		"""delete from `tabVariant Field`
			where field_name in ('attributes', 'has_variants')"""
	)
