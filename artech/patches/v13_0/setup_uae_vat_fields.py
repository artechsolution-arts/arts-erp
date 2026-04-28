# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import artech_engine

from artech.regional.united_arab_emirates.setup import setup


def execute():
	company = artech_engine.get_all("Company", filters={"country": "United Arab Emirates"})
	if not company:
		return

	artech_engine.reload_doc("regional", "report", "uae_vat_201")
	artech_engine.reload_doc("regional", "doctype", "uae_vat_settings")
	artech_engine.reload_doc("regional", "doctype", "uae_vat_account")

	setup()
