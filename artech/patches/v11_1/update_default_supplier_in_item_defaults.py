import artech_engine


def execute():
	"""
	default supplier was not set in the item defaults for multi company instance,
	        this patch will set the default supplier

	"""
	if not artech_engine.db.has_column("Item", "default_supplier"):
		return

	artech_engine.reload_doc("stock", "doctype", "item_default")
	artech_engine.reload_doc("stock", "doctype", "item")

	companies = artech_engine.get_all("Company")
	if len(companies) > 1:
		artech_engine.db.sql(
			""" UPDATE `tabItem Default`, `tabItem`
			SET `tabItem Default`.default_supplier = `tabItem`.default_supplier
			WHERE
				`tabItem Default`.parent = `tabItem`.name and `tabItem Default`.default_supplier is null
				and `tabItem`.default_supplier is not null and `tabItem`.default_supplier != '' """
		)
