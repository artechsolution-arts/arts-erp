import artech_engine


@artech_engine.whitelist()
def get_first_lead():
	lead = artech_engine.get_all(
		"CRM Lead",
		filters={"converted": 0},
		fields=["name"],
		order_by="creation",
		limit=1,
	)
	return lead[0].name if lead else None


@artech_engine.whitelist()
def get_first_deal():
	deal = artech_engine.get_all(
		"CRM Deal",
		fields=["name"],
		order_by="creation",
		limit=1,
	)
	return deal[0].name if deal else None
