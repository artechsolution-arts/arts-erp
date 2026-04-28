import artech_engine


def execute():
	if artech_engine.db.has_table("Tax Withholding Category") and artech_engine.db.has_column(
		"Tax Withholding Category", "round_off_tax_amount"
	):
		artech_engine.db.sql(
			"""
			UPDATE `tabTax Withholding Category` set round_off_tax_amount = 0
			WHERE round_off_tax_amount IS NULL
		"""
		)
