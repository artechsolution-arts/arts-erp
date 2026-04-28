import artech_engine


def execute():
	artech_engine.reload_doctype("Pricing Rule")

	currency = artech_engine.db.get_default("currency")
	for doc in artech_engine.get_all("Pricing Rule", fields=["company", "name"]):
		if doc.company:
			currency = artech_engine.get_cached_value("Company", doc.company, "default_currency")

		artech_engine.db.sql("""update `tabPricing Rule` set currency = %s where name = %s""", (currency, doc.name))
