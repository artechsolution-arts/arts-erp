import artech_engine


def execute():
	# Erase all default item manufacturers that dont exist.
	item = artech_engine.qb.DocType("Item")
	manufacturer = artech_engine.qb.DocType("Manufacturer")

	(
		artech_engine.qb.update(item)
		.set(item.default_item_manufacturer, None)
		.left_join(manufacturer)
		.on(item.default_item_manufacturer == manufacturer.name)
		.where(manufacturer.name.isnull() & item.default_item_manufacturer.isnotnull())
	).run()
