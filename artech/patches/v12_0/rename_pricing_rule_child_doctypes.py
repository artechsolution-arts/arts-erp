# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine

doctypes = {
	"Price Discount Slab": "Promotional Scheme Price Discount",
	"Product Discount Slab": "Promotional Scheme Product Discount",
	"Apply Rule On Item Code": "Pricing Rule Item Code",
	"Apply Rule On Item Group": "Pricing Rule Item Group",
	"Apply Rule On Brand": "Pricing Rule Brand",
}


def execute():
	for old_doc, new_doc in doctypes.items():
		if not artech_engine.db.table_exists(new_doc) and artech_engine.db.table_exists(old_doc):
			artech_engine.rename_doc("DocType", old_doc, new_doc)
			artech_engine.reload_doc("accounts", "doctype", artech_engine.scrub(new_doc))
			artech_engine.delete_doc("DocType", old_doc)
