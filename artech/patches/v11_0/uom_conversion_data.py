import artech_engine


def execute():
	from artech.setup.setup_wizard.operations.install_fixtures import add_uom_data

	artech_engine.reload_doc("setup", "doctype", "UOM Conversion Factor")
	artech_engine.reload_doc("setup", "doctype", "UOM")
	artech_engine.reload_doc("stock", "doctype", "UOM Category")

	if not artech_engine.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		artech_engine.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			artech_engine.delete_doc("UOM", "Hundredweight")
			artech_engine.delete_doc("UOM", "Pound Cubic Yard")
		except artech_engine.LinkExistsError:
			pass

		add_uom_data()
