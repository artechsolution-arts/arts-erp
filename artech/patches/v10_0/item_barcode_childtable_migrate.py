import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "item_barcode")
	if artech_engine.get_all("Item Barcode", limit=1):
		return
	if "barcode" not in artech_engine.db.get_table_columns("Item"):
		return

	items_barcode = artech_engine.db.sql("select name, barcode from tabItem where barcode is not null", as_dict=True)
	artech_engine.reload_doc("stock", "doctype", "item")

	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and "<" not in barcode:
			try:
				artech_engine.get_doc(
					{
						"idx": 0,
						"doctype": "Item Barcode",
						"barcode": barcode,
						"parenttype": "Item",
						"parent": item.name,
						"parentfield": "barcodes",
					}
				).insert()
			except (artech_engine.DuplicateEntryError, artech_engine.UniqueValidationError):
				continue
