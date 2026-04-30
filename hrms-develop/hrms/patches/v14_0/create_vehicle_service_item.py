import artech_engine


def execute():
	service_items = [
		"Brake Oil",
		"Brake Pad",
		"Clutch Plate",
		"Engine Oil",
		"Oil Change",
		"Wheels",
	]
	for item in service_items:
		doc = artech_engine.new_doc("Vehicle Service Item")
		doc.service_item = item
		doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
