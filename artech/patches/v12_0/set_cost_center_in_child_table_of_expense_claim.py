import artech_engine


def execute():
	artech_engine.reload_doc("hr", "doctype", "expense_claim_detail")
	artech_engine.db.sql(
		"""
		UPDATE `tabExpense Claim Detail` child, `tabExpense Claim` par
		SET child.cost_center = par.cost_center
		WHERE child.parent = par.name
	"""
	)
