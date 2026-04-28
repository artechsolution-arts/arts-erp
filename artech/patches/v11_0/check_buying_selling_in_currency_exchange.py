import artech_engine


def execute():
	artech_engine.reload_doc("setup", "doctype", "currency_exchange")
	artech_engine.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")
