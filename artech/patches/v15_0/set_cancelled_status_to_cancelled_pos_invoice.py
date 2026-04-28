import artech_engine
from artech_engine.query_builder import DocType


def execute():
	POSInvoice = DocType("POS Invoice")

	artech_engine.qb.update(POSInvoice).set(POSInvoice.status, "Cancelled").where(POSInvoice.docstatus == 2).run()
