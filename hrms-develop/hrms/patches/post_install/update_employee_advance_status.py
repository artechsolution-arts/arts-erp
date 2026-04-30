import artech_engine


def execute():
	artech_engine.reload_doc("hr", "doctype", "employee_advance")

	advance = artech_engine.qb.DocType("Employee Advance")
	(
		artech_engine.qb.update(advance)
		.set(advance.status, "Returned")
		.where(
			(advance.docstatus == 1)
			& ((advance.return_amount) & (advance.paid_amount == advance.return_amount))
			& (advance.status == "Paid")
		)
	).run()

	(
		artech_engine.qb.update(advance)
		.set(advance.status, "Partly Claimed and Returned")
		.where(
			(advance.docstatus == 1)
			& (
				(advance.claimed_amount & advance.return_amount)
				& (advance.paid_amount == (advance.return_amount + advance.claimed_amount))
			)
			& (advance.status == "Paid")
		)
	).run()
