import artech_engine


def execute():
	artech_engine.reload_doc("manufacturing", "doctype", "job_card")
	artech_engine.reload_doc("manufacturing", "doctype", "job_card_item")
	artech_engine.reload_doc("manufacturing", "doctype", "work_order_operation")

	artech_engine.db.sql(
		""" update `tabJob Card` jc, `tabWork Order Operation` wo
		SET	jc.hour_rate =  wo.hour_rate
		WHERE
			jc.operation_id = wo.name and jc.docstatus < 2 and wo.hour_rate > 0
	"""
	)
