import artech_engine


def execute():
	if "lending" in artech_engine.get_installed_apps():
		return

	artech_engine.delete_doc("Module Def", "Loan Management", ignore_missing=True, force=True)

	artech_engine.delete_doc("Workspace", "Loans", ignore_missing=True, force=True)

	print_formats = artech_engine.get_all(
		"Print Format", {"module": "Loan Management", "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		artech_engine.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = artech_engine.get_all("Report", {"module": "Loan Management", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		artech_engine.delete_doc("Report", report, ignore_missing=True, force=True)

	doctypes = artech_engine.get_all("DocType", {"module": "Loan Management", "custom": 0}, pluck="name")
	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True, force=True)

	notifications = artech_engine.get_all(
		"Notification", {"module": "Loan Management", "is_standard": 1}, pluck="name"
	)
	for notifcation in notifications:
		artech_engine.delete_doc("Notification", notifcation, ignore_missing=True, force=True)

	for dt in ["Web Form", "Dashboard", "Dashboard Chart", "Number Card"]:
		records = artech_engine.get_all(dt, {"module": "Loan Management", "is_standard": 1}, pluck="name")
		for record in records:
			artech_engine.delete_doc(dt, record, ignore_missing=True, force=True)

	custom_fields = {
		"Loan": ["repay_from_salary"],
		"Loan Repayment": ["repay_from_salary", "payroll_payable_account"],
	}

	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = artech_engine.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			artech_engine.delete_doc("Custom Field", record, ignore_missing=True, force=True)
