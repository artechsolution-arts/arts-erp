import json

import artech_engine


def execute():
	if not artech_engine.db.exists("CRM Fields Layout", "CRM Deal-Quick Entry"):
		return

	deal = artech_engine.db.get_value("CRM Fields Layout", "CRM Deal-Quick Entry", "layout")

	layout = json.loads(deal)
	for section in layout:
		if section.get("label") in [
			"Select Organization",
			"Organization Details",
			"Select Contact",
			"Contact Details",
		]:
			section["editable"] = False

	artech_engine.db.set_value("CRM Fields Layout", "CRM Deal-Quick Entry", "layout", json.dumps(layout))
