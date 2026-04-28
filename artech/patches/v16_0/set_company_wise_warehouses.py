import artech_engine


def execute():
	warehouses = artech_engine.get_single_value(
		"Manufacturing Settings",
		["default_wip_warehouse", "default_fg_warehouse", "default_scrap_warehouse"],
		as_dict=True,
	)

	for name, warehouse in warehouses.items():
		if warehouse:
			company = artech_engine.get_value("Warehouse", warehouse, "company")
			artech_engine.db.set_value("Company", company, name, warehouse)
