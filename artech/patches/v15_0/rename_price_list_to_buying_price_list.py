import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	if artech_engine.db.has_column("Material Request", "price_list"):
		rename_field(
			"Material Request",
			"price_list",
			"buying_price_list",
		)
