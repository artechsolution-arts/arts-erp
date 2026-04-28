import artech_engine

from artech.setup.install import setup_currency_exchange


def execute():
	artech_engine.reload_doc("accounts", "doctype", "currency_exchange_settings")
	setup_currency_exchange()
