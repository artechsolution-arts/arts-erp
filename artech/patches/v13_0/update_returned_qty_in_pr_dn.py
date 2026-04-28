import artech_engine

from artech.controllers.status_updater import OverAllowanceError


def execute():
	artech_engine.reload_doc("stock", "doctype", "purchase_receipt")
	artech_engine.reload_doc("stock", "doctype", "purchase_receipt_item")
	artech_engine.reload_doc("stock", "doctype", "delivery_note")
	artech_engine.reload_doc("stock", "doctype", "delivery_note_item")
	artech_engine.reload_doc("stock", "doctype", "stock_settings")

	def update_from_return_docs(doctype):
		for return_doc in artech_engine.get_all(
			doctype, filters={"is_return": 1, "docstatus": 1, "return_against": ("!=", "")}
		):
			# Update original receipt/delivery document from return
			return_doc = artech_engine.get_cached_doc(doctype, return_doc.name)
			try:
				return_doc.update_prevdoc_status()
			except OverAllowanceError:
				artech_engine.db.rollback()
				continue

			return_against = artech_engine.get_doc(doctype, return_doc.return_against)
			return_against.update_billing_status()
			artech_engine.db.commit()

	# Set received qty in stock uom in PR, as returned qty is checked against it
	artech_engine.db.sql(
		""" update `tabPurchase Receipt Item`
		set received_stock_qty = received_qty * conversion_factor
		where docstatus = 1 """
	)

	for doctype in ("Purchase Receipt", "Delivery Note"):
		update_from_return_docs(doctype)
