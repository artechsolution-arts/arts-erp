import artech_engine


def execute():
	valuation_method = artech_engine.get_single_value("Stock Settings", "valuation_method")
	for company in artech_engine.get_all("Company", pluck="name"):
		artech_engine.db.set_value("Company", company, "valuation_method", valuation_method)
