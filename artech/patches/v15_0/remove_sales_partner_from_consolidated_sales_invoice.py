import artech_engine


def execute():
	SalesInvoice = artech_engine.qb.DocType("Sales Invoice")

	query = (
		artech_engine.qb.update(SalesInvoice)
		.set(SalesInvoice.sales_partner, "")
		.set(SalesInvoice.commission_rate, 0)
		.set(SalesInvoice.total_commission, 0)
		.where(SalesInvoice.is_consolidated == 1)
	)

	# For develop/version-16
	if artech_engine.db.has_column("Sales Invoice", "is_created_using_pos"):
		query = query.where(SalesInvoice.is_created_using_pos == 0)

	query.run()
