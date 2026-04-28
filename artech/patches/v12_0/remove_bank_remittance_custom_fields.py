import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "tax_category")
	artech_engine.reload_doc("stock", "doctype", "item_manufacturer")
	company = artech_engine.get_all("Company", filters={"country": "India"})
	if not company:
		return
	if artech_engine.db.exists("Custom Field", "Company-bank_remittance_section"):
		deprecated_fields = [
			"bank_remittance_section",
			"client_code",
			"remittance_column_break",
			"product_code",
		]
		for i in range(len(deprecated_fields)):
			artech_engine.delete_doc("Custom Field", "Company-" + deprecated_fields[i])
