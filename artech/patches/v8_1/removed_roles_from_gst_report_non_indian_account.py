# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	if artech_engine.db.exists("Company", {"country": "India"}):
		return

	artech_engine.reload_doc("core", "doctype", "has_role")
	artech_engine.db.sql(
		"""
		delete from
			`tabHas Role`
		where
			parenttype = 'Report' and parent in('GST Sales Register',
				'GST Purchase Register', 'GST Itemised Sales Register',
				'GST Itemised Purchase Register', 'Eway Bill')
		"""
	)
