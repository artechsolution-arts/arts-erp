import artech_engine


def execute():
	doctype = "Stock Reconciliation Item"

	if not artech_engine.db.has_column(doctype, "current_serial_no"):
		# nothing to fix if column doesn't exist
		return

	sr_item = artech_engine.qb.DocType(doctype)

	(artech_engine.qb.update(sr_item).set(sr_item.current_serial_no, None).where(sr_item.current_qty == 0)).run()
