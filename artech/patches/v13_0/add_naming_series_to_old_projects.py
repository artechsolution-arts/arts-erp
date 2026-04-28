import artech_engine


def execute():
	artech_engine.reload_doc("projects", "doctype", "project")

	artech_engine.db.sql(
		"""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL"""
	)
