import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	if artech_engine.db.has_column("Delivery Stop", "lock"):
		rename_field("Delivery Stop", "lock", "locked")
