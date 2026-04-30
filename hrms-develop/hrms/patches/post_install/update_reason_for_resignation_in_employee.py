# MIT License. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("setup", "doctype", "employee")

	if artech_engine.db.has_column("Employee", "reason_for_resignation"):
		artech_engine.db.sql(
			""" UPDATE `tabEmployee`
            SET reason_for_leaving = reason_for_resignation
            WHERE status = 'Left' and reason_for_leaving is null and reason_for_resignation is not null
        """
		)
