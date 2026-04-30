import artech_engine


def execute():
	artech_engine.clear_cache(doctype="Leave Type")

	if artech_engine.db.has_column("Leave Type", "based_on_date_of_joining"):
		LeaveType = artech_engine.qb.DocType("Leave Type")
		artech_engine.qb.update(LeaveType).set(LeaveType.allocate_on_day, "Last Day").where(
			(LeaveType.based_on_date_of_joining == 0) & (LeaveType.is_earned_leave == 1)
		).run()

		artech_engine.qb.update(LeaveType).set(LeaveType.allocate_on_day, "Date of Joining").where(
			LeaveType.based_on_date_of_joining == 1
		).run()

		artech_engine.db.sql_ddl("alter table `tabLeave Type` drop column `based_on_date_of_joining`")
		# clear cache for doctype as it stores table columns in cache
		artech_engine.clear_cache(doctype="Leave Type")
