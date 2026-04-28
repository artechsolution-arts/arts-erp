import artech_engine


def execute():
	artech_engine.reload_doc("setup", "doctype", "company")

	companies = artech_engine.get_all("Company", fields=["name", "default_payable_account"])

	for company in companies:
		if company.default_payable_account is not None:
			artech_engine.db.set_value(
				"Company",
				company.name,
				"default_expense_claim_payable_account",
				company.default_payable_account,
			)
