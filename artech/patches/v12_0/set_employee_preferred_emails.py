import artech_engine


def execute():
	employees = artech_engine.get_all(
		"Employee",
		filters={"prefered_email": ""},
		fields=["name", "prefered_contact_email", "company_email", "personal_email", "user_id"],
	)

	for employee in employees:
		if not employee.prefered_contact_email:
			continue

		preferred_email_field = artech_engine.scrub(employee.prefered_contact_email)

		preferred_email = employee.get(preferred_email_field)
		artech_engine.db.set_value(
			"Employee", employee.name, "prefered_email", preferred_email, update_modified=False
		)
