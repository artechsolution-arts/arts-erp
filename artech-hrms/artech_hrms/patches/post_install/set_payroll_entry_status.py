import artech_engine


def execute():
	PayrollEntry = artech_engine.qb.DocType("Payroll Entry")

	status = (
		artech_engine.qb.terms.Case()
		.when(PayrollEntry.docstatus == 0, "Draft")
		.when(PayrollEntry.docstatus == 1, "Submitted")
		.else_("Cancelled")
	)

	(artech_engine.qb.update(PayrollEntry).set("status", status).where(PayrollEntry.status.isnull())).run()
