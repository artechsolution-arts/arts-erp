import artech_engine


def execute():
	# handle type casting for is_cancelled field
	module_doctypes = (
		("stock", "Stock Ledger Entry"),
		("stock", "Serial No"),
		("accounts", "GL Entry"),
	)

	for module, doctype in module_doctypes:
		if (
			not artech_engine.db.has_column(doctype, "is_cancelled")
			or artech_engine.db.get_column_type(doctype, "is_cancelled").lower() == "int(1)"
		):
			continue

		artech_engine.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 0
				where is_cancelled in ('', 'No') or is_cancelled is NULL"""
		)
		artech_engine.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 1
				where is_cancelled = 'Yes'"""
		)

		artech_engine.reload_doc(module, "doctype", artech_engine.scrub(doctype))
