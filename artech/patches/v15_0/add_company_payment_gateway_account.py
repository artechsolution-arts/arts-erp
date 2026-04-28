import artech_engine


def execute():
	for gateway_account in artech_engine.get_list("Payment Gateway Account", fields=["name", "payment_account"]):
		company = artech_engine.db.get_value("Account", gateway_account.payment_account, "company")
		artech_engine.db.set_value("Payment Gateway Account", gateway_account.name, "company", company)
