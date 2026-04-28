import artech_engine


def execute():
	artech_engine.db.sql(
		"""
		UPDATE `tabStock Ledger Entry`
			SET posting_datetime = timestamp(posting_date, posting_time)
	"""
	)
