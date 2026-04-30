import artech_engine


def execute():
	artech_engine.reload_doc("hr", "doctype", "shift_assignment")
	if artech_engine.db.has_column("Shift Assignment", "date"):
		artech_engine.db.sql(
			"""update `tabShift Assignment`
            set end_date=date, start_date=date
            where date IS NOT NULL and start_date IS NULL and end_date IS NULL;"""
		)
