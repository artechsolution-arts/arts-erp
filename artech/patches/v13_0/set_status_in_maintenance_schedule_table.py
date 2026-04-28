import artech_engine


def execute():
	artech_engine.reload_doc("maintenance", "doctype", "Maintenance Schedule Detail")
	artech_engine.db.sql(
		"""
		UPDATE `tabMaintenance Schedule Detail`
		SET completion_status = 'Pending'
		WHERE docstatus < 2
	"""
	)
