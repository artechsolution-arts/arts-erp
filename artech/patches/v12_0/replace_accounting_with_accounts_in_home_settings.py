import artech_engine


def execute():
	artech_engine.db.sql(
		"""UPDATE `tabUser` SET `home_settings` = REPLACE(`home_settings`, 'Accounting', 'Accounts')"""
	)
	artech_engine.cache().delete_key("home_settings")
