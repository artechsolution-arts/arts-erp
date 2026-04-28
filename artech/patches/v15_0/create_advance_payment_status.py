import artech_engine


def execute():
	"""
	Description:
	Calculate the new Advance Payment Statuse column in SO & PO
	"""

	if artech_engine.reload_doc("selling", "doctype", "Sales Order"):
		so = artech_engine.qb.DocType("Sales Order")
		artech_engine.qb.update(so).set(so.advance_payment_status, "Not Requested").where(so.docstatus == 1).where(
			so.advance_paid == 0.0
		).run()

		artech_engine.qb.update(so).set(so.advance_payment_status, "Partially Paid").where(so.docstatus == 1).where(
			so.advance_payment_status.isnull()
		).where(so.advance_paid < (so.rounded_total or so.grand_total)).run()

		artech_engine.qb.update(so).set(so.advance_payment_status, "Fully Paid").where(so.docstatus == 1).where(
			so.advance_payment_status.isnull()
		).where(so.advance_paid == (so.rounded_total or so.grand_total)).run()

		pr = artech_engine.qb.DocType("Payment Request")
		artech_engine.qb.update(so).join(pr).on(so.name == pr.reference_name).set(
			so.advance_payment_status, "Requested"
		).where(so.docstatus == 1).where(pr.docstatus == 1).where(
			so.advance_payment_status == "Not Requested"
		).run()

	if artech_engine.reload_doc("buying", "doctype", "Purchase Order"):
		po = artech_engine.qb.DocType("Purchase Order")
		artech_engine.qb.update(po).set(po.advance_payment_status, "Not Initiated").where(po.docstatus == 1).where(
			po.advance_paid == 0.0
		).run()

		artech_engine.qb.update(po).set(po.advance_payment_status, "Partially Paid").where(po.docstatus == 1).where(
			po.advance_payment_status.isnull()
		).where(po.advance_paid < (po.rounded_total or po.grand_total)).run()

		artech_engine.qb.update(po).set(po.advance_payment_status, "Fully Paid").where(po.docstatus == 1).where(
			po.advance_payment_status.isnull()
		).where(po.advance_paid == (po.rounded_total or po.grand_total)).run()

		pr = artech_engine.qb.DocType("Payment Request")
		artech_engine.qb.update(po).join(pr).on(po.name == pr.reference_name).set(
			po.advance_payment_status, "Initiated"
		).where(po.docstatus == 1).where(pr.docstatus == 1).where(
			po.advance_payment_status == "Not Initiated"
		).run()
