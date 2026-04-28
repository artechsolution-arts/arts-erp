import artech_engine


def execute():
	artech_engine.reload_doc("manufacturing", "doctype", "workstation")

	artech_engine.db.sql(
		""" UPDATE `tabWorkstation`
        SET production_capacity = 1 """
	)
