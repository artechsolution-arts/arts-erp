import artech_engine


def execute():
	artech_engine.reload_doc("HR", "doctype", "Leave Allocation")
	artech_engine.reload_doc("HR", "doctype", "Leave Ledger Entry")
	artech_engine.db.sql(
		"""
		UPDATE `tabLeave Ledger Entry` as lle
		SET company = (select company from `tabEmployee` where employee = lle.employee)
		WHERE company IS NULL
		"""
	)
	artech_engine.db.sql(
		"""
		UPDATE `tabLeave Allocation` as la
		SET company = (select company from `tabEmployee` where employee = la.employee)
		WHERE company IS NULL
		"""
	)
