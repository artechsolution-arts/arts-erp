import artech_engine


def execute():
	if artech_engine.get_all("Company", filters={"country": "India"}, limit=1):
		artech_engine.db.set_single_value("Stock Settings", "allow_existing_serial_no", 1)
