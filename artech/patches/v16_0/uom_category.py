import json

import artech_engine


def execute():
	uom_data = json.loads(
		open(artech_engine.get_app_path("artech", "setup", "setup_wizard", "data", "uom_data.json")).read()
	)
	bulk_update_dict = {uom["uom_name"]: {"category": uom["category"]} for uom in uom_data}
	artech_engine.db.bulk_update("UOM", bulk_update_dict)
