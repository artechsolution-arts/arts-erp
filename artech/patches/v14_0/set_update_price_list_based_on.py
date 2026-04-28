import artech_engine
from artech_engine.utils import cint


def execute():
	artech_engine.db.set_single_value(
		"Stock Settings",
		"update_price_list_based_on",
		(
			"Price List Rate"
			if cint(artech_engine.db.get_single_value("Selling Settings", "editable_price_list_rate"))
			else "Rate"
		),
	)
