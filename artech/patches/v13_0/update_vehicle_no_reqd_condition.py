import artech_engine


def execute():
	artech_engine.reload_doc("custom", "doctype", "custom_field", force=True)
	company = artech_engine.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if artech_engine.db.exists("Custom Field", {"fieldname": "vehicle_no"}):
		artech_engine.db.set_value("Custom Field", {"fieldname": "vehicle_no"}, "mandatory_depends_on", "")
