# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "subscription")
	artech_engine.reload_doc("accounts", "doctype", "subscription_invoice")
	artech_engine.reload_doc("accounts", "doctype", "subscription_plan")

	if artech_engine.db.has_column("Subscription", "customer"):
		artech_engine.db.sql(
			"""
			UPDATE `tabSubscription`
			SET
				start_date = start,
				party_type = 'Customer',
				party = customer,
				sales_tax_template = tax_template
			WHERE IFNULL(party,'') = ''
		"""
		)

	artech_engine.db.sql(
		"""
		UPDATE `tabSubscription Invoice`
		SET document_type = 'Sales Invoice'
		WHERE IFNULL(document_type, '') = ''
	"""
	)

	price_determination_map = {
		"Fixed rate": "Fixed Rate",
		"Based on price list": "Based On Price List",
	}

	for key, value in price_determination_map.items():
		artech_engine.db.sql(
			"""
			UPDATE `tabSubscription Plan`
			SET price_determination = %s
			WHERE price_determination = %s
		""",
			(value, key),
		)
