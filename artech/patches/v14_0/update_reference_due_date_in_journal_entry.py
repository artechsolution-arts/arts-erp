import artech_engine


def execute():
	if artech_engine.db.get_value("Journal Entry Account", {"reference_due_date": ""}):
		artech_engine.db.sql(
			"""
			UPDATE `tabJournal Entry Account`
			SET reference_due_date = NULL
			WHERE reference_due_date = ''
		"""
		)
