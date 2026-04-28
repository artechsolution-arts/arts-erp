import artech_engine


def execute():
	name = artech_engine.db.sql(
		""" select name from `tabPatch Log` \
		where \
			patch like 'execute:artech_engine.db.sql("update `tabProduction Order` pro set description%' """
	)
	if not name:
		artech_engine.db.sql(
			"update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''"
		)
