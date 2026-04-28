# Copyright (c) 2018, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.reload_doc("manufacturing", "doctype", "manufacturing_settings")
	rename_field(
		"Manufacturing Settings",
		"over_production_allowance_percentage",
		"overproduction_percentage_for_sales_order",
	)
