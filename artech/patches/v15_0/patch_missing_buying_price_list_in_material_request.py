import artech_engine
import artech_engine.defaults


def execute():
	if artech_engine.db.has_column("Material Request", "buying_price_list") and (
		default_buying_price_list := artech_engine.defaults.get_defaults().buying_price_list
	):
		docs = artech_engine.get_all(
			"Material Request", filters={"buying_price_list": ["is", "not set"], "docstatus": 1}, pluck="name"
		)
		artech_engine.db.auto_commit_on_many_writes = 1
		try:
			for doc in docs:
				artech_engine.db.set_value("Material Request", doc, "buying_price_list", default_buying_price_list)
		finally:
			artech_engine.db.auto_commit_on_many_writes = 0
