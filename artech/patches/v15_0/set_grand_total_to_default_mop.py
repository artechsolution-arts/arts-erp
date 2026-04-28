import artech_engine


def execute():
	if artech_engine.db.has_column("POS Profile", "disable_grand_total_to_default_mop"):
		POSProfile = artech_engine.qb.DocType("POS Profile")

		artech_engine.qb.update(POSProfile).set(POSProfile.set_grand_total_to_default_mop, 1).where(
			POSProfile.disable_grand_total_to_default_mop == 0
		).run()
