import artech_engine


def execute():
	sabb = artech_engine.get_all("Serial and Batch Bundle", filters={"docstatus": ("<", 2)}, limit=1)
	if not sabb:
		artech_engine.db.set_single_value("Stock Settings", "use_serial_batch_fields", 1)
