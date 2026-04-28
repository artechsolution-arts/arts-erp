import artech_engine


def execute():
	artech_engine.reload_doc("crm", "doctype", "lead")
	artech_engine.db.sql(
		"""
		UPDATE
			`tabLead`
		SET
			title = IF(organization_lead = 1, company_name, lead_name)
	"""
	)
