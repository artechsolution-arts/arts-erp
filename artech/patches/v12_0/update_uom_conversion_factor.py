import artech_engine


def execute():
	from artech.setup.setup_wizard.operations.install_fixtures import add_uom_data

	artech_engine.reload_doc("setup", "doctype", "UOM Conversion Factor")
	artech_engine.reload_doc("setup", "doctype", "UOM")
	artech_engine.reload_doc("stock", "doctype", "UOM Category")

	add_uom_data()
