import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "pricing_rule")

	artech_engine.db.sql(
		""" UPDATE `tabPricing Rule` SET price_or_product_discount = 'Price'
		WHERE ifnull(price_or_product_discount,'') = '' """
	)
