import artech_engine


def execute():
	artech_engine.reload_doc("selling", "doctype", "sales_order_item", force=True)
	artech_engine.reload_doc("buying", "doctype", "purchase_order_item", force=True)

	for doctype in ("Sales Order Item", "Purchase Order Item"):
		artech_engine.db.sql(
			f"""
			UPDATE `tab{doctype}`
			SET against_blanket_order = 1
			WHERE ifnull(blanket_order, '') != ''
		"""
		)
