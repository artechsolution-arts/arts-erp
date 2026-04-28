import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "batch")

	for batch in artech_engine.get_all("Batch", fields=["name", "batch_id"]):
		batch_qty = (
			artech_engine.db.get_value(
				"Stock Ledger Entry",
				{"docstatus": 1, "batch_no": batch.batch_id, "is_cancelled": 0},
				[{"SUM": "actual_qty"}],
			)
			or 0.0
		)
		artech_engine.db.set_value("Batch", batch.name, "batch_qty", batch_qty, update_modified=False)
