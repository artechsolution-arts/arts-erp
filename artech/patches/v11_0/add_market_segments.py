import artech_engine

from artech.setup.setup_wizard.operations.install_fixtures import add_market_segments


def execute():
	artech_engine.reload_doc("crm", "doctype", "market_segment")

	artech_engine.local.lang = artech_engine.db.get_default("lang") or "en"

	add_market_segments()
