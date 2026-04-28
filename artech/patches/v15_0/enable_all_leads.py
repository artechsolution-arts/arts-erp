import artech_engine


def execute():
	lead = artech_engine.qb.DocType("Lead")
	artech_engine.qb.update(lead).set(lead.disabled, 0).set(lead.docstatus, 0).where(
		lead.disabled == 1 and lead.docstatus == 1
	).run()
