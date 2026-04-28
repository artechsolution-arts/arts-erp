import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "item_tax_template")

	item_tax_template_list = artech_engine.get_list("Item Tax Template")
	for template in item_tax_template_list:
		doc = artech_engine.get_doc("Item Tax Template", template.name)
		for tax in doc.taxes:
			doc.company = artech_engine.get_value("Account", tax.tax_type, "company")
			break
		doc.save()
