import artech_engine


def execute():
	subscription = artech_engine.qb.DocType("Subscription")
	artech_engine.qb.update(subscription).set(
		subscription.generate_invoice_at, "Beginning of the current subscription period"
	).where(subscription.generate_invoice_at_period_start == 1).run()
