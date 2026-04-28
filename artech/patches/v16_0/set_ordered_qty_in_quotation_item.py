import artech_engine


def execute():
	data = artech_engine.get_all(
		"Sales Order Item",
		filters={"quotation_item": ["is", "set"], "docstatus": 1},
		fields=["quotation_item", {"SUM": "stock_qty", "as": "ordered_qty"}],
		group_by="quotation_item",
	)
	if data:
		artech_engine.db.auto_commit_on_many_writes = 1
		artech_engine.db.bulk_update(
			"Quotation Item", {d.quotation_item: {"ordered_qty": d.ordered_qty} for d in data}
		)
		artech_engine.db.auto_commit_on_many_writes = 0
