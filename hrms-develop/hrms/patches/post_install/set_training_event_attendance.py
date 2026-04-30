import artech_engine


def execute():
	artech_engine.reload_doc("hr", "doctype", "training_event")
	artech_engine.reload_doc("hr", "doctype", "training_event_employee")

	# no need to run the update query as there is no old data
	if not artech_engine.db.exists("Training Event Employee", {"attendance": ("in", ("Mandatory", "Optional"))}):
		return

	artech_engine.db.sql(
		"""
		UPDATE `tabTraining Event Employee`
		SET is_mandatory = 1
		WHERE attendance = 'Mandatory'
		"""
	)
	artech_engine.db.sql(
		"""
		UPDATE `tabTraining Event Employee`
		SET attendance = 'Present'
		WHERE attendance in ('Mandatory', 'Optional')
	"""
	)
