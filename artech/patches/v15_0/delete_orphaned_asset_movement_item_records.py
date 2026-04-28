import artech_engine


def execute():
	# nosemgrep
	artech_engine.db.sql(
		"""
		DELETE FROM `tabAsset Movement Item`
		WHERE parent NOT IN (SELECT name FROM `tabAsset Movement`)
		"""
	)
