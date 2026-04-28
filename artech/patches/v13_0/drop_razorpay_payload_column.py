import artech_engine


def execute():
	if artech_engine.db.exists("DocType", "Membership"):
		if "webhook_payload" in artech_engine.db.get_table_columns("Membership"):
			artech_engine.db.sql("alter table `tabMembership` drop column webhook_payload")
