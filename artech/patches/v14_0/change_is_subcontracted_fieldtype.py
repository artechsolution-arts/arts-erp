# Copyright (c) 2022, Artech and contributors
# For license information, please see license.txt

import artech_engine


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice", "Supplier Quotation"]:
		artech_engine.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 0
				where is_subcontracted in ('', 'No') or is_subcontracted is null"""
		)
		artech_engine.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 1
				where is_subcontracted = 'Yes'"""
		)

		artech_engine.reload_doc(artech_engine.get_meta(doctype).module, "doctype", artech_engine.scrub(doctype))
