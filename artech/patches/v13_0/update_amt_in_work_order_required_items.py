import artech_engine


def execute():
	"""Correct amount in child table of required items table."""

	artech_engine.reload_doc("manufacturing", "doctype", "work_order")
	artech_engine.reload_doc("manufacturing", "doctype", "work_order_item")

	artech_engine.db.sql(
		"""UPDATE `tabWork Order Item` SET amount = ifnull(rate, 0.0) * ifnull(required_qty, 0.0)"""
	)
