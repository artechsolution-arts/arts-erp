# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine

from artech.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	company = artech_engine.get_all("Company", filters={"country": ["in", ["Saudi Arabia", "United Arab Emirates"]]})
	if not company:
		return

	artech_engine.reload_doc("accounts", "doctype", "pos_invoice")
	artech_engine.reload_doc("accounts", "doctype", "pos_invoice_item")

	make_custom_fields()
