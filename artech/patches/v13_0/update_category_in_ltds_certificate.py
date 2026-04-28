import artech_engine


def execute():
	company = artech_engine.get_all("Company", filters={"country": "India"})
	if not company:
		return

	artech_engine.reload_doc("regional", "doctype", "lower_deduction_certificate")

	ldc = artech_engine.qb.DocType("Lower Deduction Certificate").as_("ldc")
	supplier = artech_engine.qb.DocType("Supplier")

	artech_engine.qb.update(ldc).inner_join(supplier).on(ldc.supplier == supplier.name).set(
		ldc.tax_withholding_category, supplier.tax_withholding_category
	).where(ldc.tax_withholding_category.isnull()).run()
