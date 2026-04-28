import artech_engine

from artech.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	if not artech_engine.db.get_value("Company", {"country": "United Arab Emirates"}):
		return

	make_custom_fields()
