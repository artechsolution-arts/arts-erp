import artech_engine


def execute():
	if data := artech_engine.get_all(
		"Pick List Item",
		filters={"material_request_item": ["is", "set"], "docstatus": 1},
		fields=["material_request_item", {"SUM": "picked_qty", "as": "picked_qty"}],
		group_by="material_request_item",
	):
		data = {d.material_request_item: {"picked_qty": d.picked_qty} for d in data}
		artech_engine.db.bulk_update("Material Request Item", data)
