import artech_engine


def execute():
	if not artech_engine.db.exists("Stock Entry Type", "Disassemble"):
		artech_engine.get_doc(
			{
				"doctype": "Stock Entry Type",
				"name": "Disassemble",
				"purpose": "Disassemble",
				"is_standard": 1,
			}
		).insert(ignore_permissions=True)
