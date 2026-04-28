import artech_engine


def execute():
	if not artech_engine.db.get_single_value("POS Settings", "invoice_type"):
		artech_engine.db.set_single_value("POS Settings", "invoice_type", "POS Invoice")
