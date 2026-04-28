import artech_engine


def execute():
	bom = artech_engine.qb.DocType("BOM")

	(
		artech_engine.qb.update(bom).set(bom.transfer_material_against, "Work Order").where(bom.with_operations == 0)
	).run()
