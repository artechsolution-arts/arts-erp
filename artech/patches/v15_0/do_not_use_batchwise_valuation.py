import artech_engine


def execute():
	valuation_method = artech_engine.db.get_single_value("Stock Settings", "valuation_method")
	if valuation_method in ["FIFO", "LIFO"]:
		return

	if artech_engine.get_all("Batch", filters={"use_batchwise_valuation": 1}, limit=1):
		return

	if artech_engine.get_all("Item", filters={"has_batch_no": 1, "valuation_method": "FIFO"}, limit=1):
		return

	artech_engine.db.set_single_value("Stock Settings", "do_not_use_batchwise_valuation", 1)
