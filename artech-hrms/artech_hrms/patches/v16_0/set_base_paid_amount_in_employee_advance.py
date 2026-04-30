import artech_engine
from artech_engine.query_builder.functions import IfNull


def execute():
	EmployeeAdvance = artech_engine.qb.DocType("Employee Advance")
	Company = artech_engine.qb.DocType("Company")

	(
		artech_engine.qb.update(EmployeeAdvance)
		.join(Company)
		.on(EmployeeAdvance.company == Company.name)
		.set(EmployeeAdvance.base_paid_amount, EmployeeAdvance.paid_amount)
		.where(
			(EmployeeAdvance.currency == Company.default_currency)
			& (IfNull(EmployeeAdvance.paid_amount, 0) != 0)
			& (IfNull(EmployeeAdvance.base_paid_amount, 0) == 0)
		)
	).run()
