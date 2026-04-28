import artech_engine

from artech.setup.setup_wizard.operations.install_fixtures import add_sale_stages


def execute():
	artech_engine.reload_doc("crm", "doctype", "sales_stage")

	artech_engine.local.lang = artech_engine.db.get_default("lang") or "en"

	add_sale_stages()
