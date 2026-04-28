import artech_engine


def execute():
	for stock_entry_type in [
		"Receive from Customer",
		"Return Raw Material to Customer",
		"Subcontracting Delivery",
		"Subcontracting Return",
	]:
		if not artech_engine.db.exists("Stock Entry Type", stock_entry_type):
			artech_engine.new_doc("Stock Entry Type", purpose=stock_entry_type, is_standard=1).insert(
				set_name=stock_entry_type, ignore_permissions=True
			)
