import artech_engine


def execute():
	salary_structure = artech_engine.qb.DocType("Salary Structure")
	artech_engine.qb.update(salary_structure).set(salary_structure.payroll_frequency, "").where(
		salary_structure.salary_slip_based_on_timesheet == 1
	).run()
