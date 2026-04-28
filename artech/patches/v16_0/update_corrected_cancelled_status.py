import artech_engine


def execute():
	stock_closing_entry = artech_engine.qb.DocType("Stock Closing Entry")
	call_log = artech_engine.qb.DocType("Call Log")

	# updating stock closing entry status to cancelled from canceled
	(
		artech_engine.qb.update(stock_closing_entry)
		.set(stock_closing_entry.status, "Cancelled")
		.where(stock_closing_entry.status == "Canceled")
	).run()

	# updating call log status to cancelled from canceled
	(artech_engine.qb.update(call_log).set(call_log.status, "Cancelled").where(call_log.status == "Canceled")).run()
