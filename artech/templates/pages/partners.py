# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine

page_title = "Partners"


def get_context(context):
	partners = artech_engine.db.sql(
		"""select * from `tabSales Partner`
			where show_in_website=1 order by name asc""",
		as_dict=True,
	)

	return {"partners": partners, "title": page_title}
