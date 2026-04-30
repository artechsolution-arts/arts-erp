from pypika.terms import ValueWrapper

import artech_engine


def execute():
	employee_holiday_details = get_employee_holiday_details()
	company_holiday_details = get_company_holiday_details()
	if not (employee_holiday_details or company_holiday_details):
		return

	for entity in employee_holiday_details + company_holiday_details:
		try:
			create_holiday_list_assignment(entity)
		except Exception as e:
			artech_engine.log_error(e)


def create_holiday_list_assignment(entity_details):
	if not artech_engine.db.exists("Holiday List Assignment", entity_details):
		hla = artech_engine.new_doc("Holiday List Assignment")
		hla.update(entity_details)
		hla.save()
		hla.submit()


def get_employee_holiday_details():
	employee = artech_engine.qb.DocType("Employee")
	holiday_list = artech_engine.qb.DocType("Holiday List")
	applicable_for = ValueWrapper("Employee", "applicable_for")
	employee_holiday_details = (
		artech_engine.qb.from_(employee)
		.inner_join(holiday_list)
		.on(employee.holiday_list == holiday_list.name)
		.select(
			(employee.name).as_("assigned_to"),
			employee.holiday_list,
			holiday_list.from_date,
			holiday_list.to_date,
			employee.company,
			applicable_for,
		)
		.where(employee.status == "Active")
	).run(as_dict=True)

	return employee_holiday_details


def get_company_holiday_details():
	company = artech_engine.qb.DocType("Company")
	holiday_list = artech_engine.qb.DocType("Holiday List")
	applicable_for = ValueWrapper("Company", "applicable_for")
	company_holiday_details = (
		artech_engine.qb.from_(company)
		.inner_join(holiday_list)
		.on(company.default_holiday_list == holiday_list.name)
		.select(
			(company.name).as_("assigned_to"),
			(company.default_holiday_list).as_("holiday_list"),
			holiday_list.from_date,
			holiday_list.to_date,
			applicable_for,
		)
	).run(as_dict=True)

	return company_holiday_details
