import artech_engine


def execute():
	artech_engine.reload_doc("setup", "doctype", "party_type")
	party_types = {
		"Customer": "Receivable",
		"Supplier": "Payable",
		"Employee": "Payable",
		"Member": "Receivable",
		"Shareholder": "Payable",
	}

	for party_type, account_type in party_types.items():
		artech_engine.db.set_value("Party Type", party_type, "account_type", account_type)
