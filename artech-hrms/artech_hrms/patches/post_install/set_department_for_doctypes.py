import artech_engine

# Set department value based on employee value


def execute():
	doctypes_to_update = {
		"hr": [
			"Appraisal",
			"Leave Allocation",
			"Expense Claim",
			"Salary Slip",
			"Attendance",
			"Training Feedback",
			"Training Result Employee",
			"Leave Application",
			"Employee Advance",
			"Training Event Employee",
			"Payroll Employee Detail",
		],
		"education": ["Instructor"],
		"projects": ["Activity Cost", "Timesheet"],
		"setup": ["Sales Person"],
	}

	for module, doctypes in doctypes_to_update.items():
		for doctype in doctypes:
			if artech_engine.db.table_exists(doctype):
				artech_engine.reload_doc(module, "doctype", artech_engine.scrub(doctype))
				artech_engine.db.sql(
					f"""
					update `tab{doctype}` dt
					set department=(select department from `tabEmployee` where name=dt.employee)
					where coalesce(`tab{doctype}`.`department`, '') = ''
					"""
				)
