# Copyright (c) 2018, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "item")
	artech_engine.db.sql(
		""" update `tabItem` set include_item_in_manufacturing = 1
		where ifnull(is_stock_item, 0) = 1"""
	)

	for doctype in ["BOM Item", "Work Order Item", "BOM Explosion Item"]:
		artech_engine.reload_doc("manufacturing", "doctype", artech_engine.scrub(doctype))

		artech_engine.db.sql(
			f""" update `tab{doctype}` child, tabItem item
			set
				child.include_item_in_manufacturing = 1
			where
				child.item_code = item.name and ifnull(item.is_stock_item, 0) = 1
		"""
		)
