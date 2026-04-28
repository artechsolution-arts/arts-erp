import artech_engine


def execute():
	subscription_invoices = artech_engine.get_all(
		"Subscription Invoice", fields=["document_type", "invoice", "parent"]
	)

	for subscription_invoice in subscription_invoices:
		artech_engine.db.set_value(
			subscription_invoice.document_type,
			subscription_invoice.invoice,
			"subscription",
			subscription_invoice.parent,
			update_modified=False,
		)

	artech_engine.delete_doc_if_exists("DocType", "Subscription Invoice", force=1)
