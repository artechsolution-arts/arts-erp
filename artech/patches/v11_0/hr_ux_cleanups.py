import artech_engine


def execute():
	artech_engine.reload_doctype("Employee")
	artech_engine.db.sql("update tabEmployee set first_name = employee_name")

	# update holiday list
	artech_engine.reload_doctype("Holiday List")
	for holiday_list in artech_engine.get_all("Holiday List"):
		holiday_list = artech_engine.get_doc("Holiday List", holiday_list.name)
		holiday_list.db_set("total_holidays", len(holiday_list.holidays), update_modified=False)
