import artech_engine


def execute():
	if not artech_engine.get_all("Serial No", limit=1) and not artech_engine.get_all("Batch", limit=1):
		return

	artech_engine.db.set_single_value("Stock Settings", "enable_serial_and_batch_no_for_item", 1)
	artech_engine.db.set_default("enable_serial_and_batch_no_for_item", 1)
