import artech_engine

from hrms.hr.doctype.shift_schedule.shift_schedule import get_or_insert_shift_schedule


def execute():
	if not artech_engine.db.has_table("Shift Assignment Schedule"):
		return

	fields = ["name", "shift_type", "frequency", "employee", "shift_status", "enabled", "create_shifts_after"]
	for doc in artech_engine.get_all("Shift Assignment Schedule", fields=fields):
		repeat_on_days = artech_engine.get_all(
			"Assignment Rule Day", {"parent": doc.name}, pluck="day", distinct=True
		)
		shift_schedule_name = get_or_insert_shift_schedule(doc.shift_type, doc.frequency, repeat_on_days)

		schedule_assignment = artech_engine.get_doc(
			{
				"doctype": "Shift Schedule Assignment",
				"shift_schedule": shift_schedule_name,
				"employee": doc.employee,
				"shift_status": doc.shift_status,
				"enabled": doc.enabled,
				"create_shifts_after": doc.create_shifts_after,
			}
		).insert()

		for d in artech_engine.get_all("Shift Assignment", filters={"schedule": doc.name}, pluck="name"):
			artech_engine.db.set_value("Shift Assignment", d, "shift_schedule_assignment", schedule_assignment.name)
