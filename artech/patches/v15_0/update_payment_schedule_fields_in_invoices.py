import artech_engine
from artech_engine.query_builder import DocType


def execute():
	invoice_types = ["Sales Invoice", "Purchase Invoice"]
	for invoice_type in invoice_types:
		invoice = DocType(invoice_type)
		invoice_details = artech_engine.qb.from_(invoice).select(invoice.conversion_rate, invoice.name)
		update_payment_schedule(invoice_details)


def update_payment_schedule(invoice_details):
	ps = DocType("Payment Schedule")

	artech_engine.qb.update(ps).join(invoice_details).on(ps.parent == invoice_details.name).set(
		ps.base_paid_amount, ps.paid_amount * invoice_details.conversion_rate
	).set(ps.base_outstanding, ps.outstanding * invoice_details.conversion_rate).run()
