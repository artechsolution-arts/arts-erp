import artech_engine


def execute():
	artech_engine.reload_doctype("Payment Entry")
	artech_engine.db.sql(
		"""update `tabPayment Entry` set status = CASE
		WHEN docstatus = 1 THEN 'Submitted'
		WHEN docstatus = 2 THEN 'Cancelled'
		ELSE 'Draft'
		END;"""
	)
