import artech_engine


def execute():
	if artech_engine.db.exists("DocType", "Member"):
		artech_engine.reload_doc("Non Profit", "doctype", "Member")

		if artech_engine.db.has_column("Member", "subscription_activated"):
			artech_engine.db.sql(
				'UPDATE `tabMember` SET subscription_status = "Active" WHERE subscription_activated = 1'
			)
			artech_engine.db.sql_ddl("ALTER table `tabMember` DROP COLUMN subscription_activated")
