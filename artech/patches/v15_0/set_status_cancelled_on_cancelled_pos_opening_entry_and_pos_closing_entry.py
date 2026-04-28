import artech_engine
from artech_engine.query_builder import DocType


def execute():
	POSOpeningEntry = DocType("POS Opening Entry")
	POSClosingEntry = DocType("POS Closing Entry")

	artech_engine.qb.update(POSOpeningEntry).set(POSOpeningEntry.status, "Cancelled").where(
		POSOpeningEntry.docstatus == 2
	).run()
	artech_engine.qb.update(POSClosingEntry).set(POSClosingEntry.status, "Cancelled").where(
		POSClosingEntry.docstatus == 2
	).run()
