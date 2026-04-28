import artech_engine

# Set department value based on employee value


def execute():
	doctypes_to_update = {
		"projects": ["Activity Cost", "Timesheet"],
		"setup": ["Sales Person"],
	}

	for module, doctypes in doctypes_to_update.items():
		for doctype in doctypes:
			if artech_engine.db.table_exists(doctype):
				artech_engine.reload_doc(module, "doctype", artech_engine.scrub(doctype))
				artech_engine.db.sql(
					"""
					update `tab%s` dt
					set department=(select department from `tabEmployee` where name=dt.employee)
				"""
					% doctype
				)
