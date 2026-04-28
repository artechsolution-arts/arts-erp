# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("buying", "doctype", "request_for_quotation_item")

	artech_engine.db.sql(
		"""UPDATE `tabRequest for Quotation Item`
			SET
				stock_uom = uom,
				conversion_factor = 1,
				stock_qty = qty"""
	)
