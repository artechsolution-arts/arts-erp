import artech_engine


def execute():
	artech_engine.reload_doc("setup", "doctype", "uom")

	uom = artech_engine.qb.DocType("UOM")

	(
		artech_engine.qb.update(uom)
		.set(uom.enabled, 1)
		.where(uom.creation >= "2021-10-18")  # date when this field was released
	).run()
