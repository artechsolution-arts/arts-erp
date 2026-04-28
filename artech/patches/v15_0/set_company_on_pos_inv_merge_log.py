import artech_engine


def execute():
	pos_invoice_merge_logs = artech_engine.db.get_all(
		"POS Invoice Merge Log", {"docstatus": 1}, ["name", "pos_closing_entry"]
	)

	artech_engine.db.auto_commit_on_many_writes = 1
	for log in pos_invoice_merge_logs:
		if log.pos_closing_entry and artech_engine.db.exists("POS Closing Entry", log.pos_closing_entry):
			company = artech_engine.db.get_value("POS Closing Entry", log.pos_closing_entry, "company")
			artech_engine.db.set_value("POS Invoice Merge Log", log.name, "company", company)

	artech_engine.db.auto_commit_on_many_writes = 0
