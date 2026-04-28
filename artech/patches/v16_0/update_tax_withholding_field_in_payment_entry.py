import artech_engine
from artech_engine.query_builder import DocType


def execute():
	if not artech_engine.db.has_column("Payment Entry", "apply_tax_withholding_amount"):
		return

	pe = DocType("Payment Entry")
	(artech_engine.qb.update(pe).set(pe.apply_tds, pe.apply_tax_withholding_amount)).run()
