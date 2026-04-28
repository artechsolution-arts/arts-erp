import artech_engine


def execute():
	"""`sales_invoice` field from loyalty point entry is splitted into `invoice_type` & `invoice` fields"""

	artech_engine.reload_doc("Accounts", "doctype", "loyalty_point_entry")

	if not artech_engine.db.has_column("Loyalty Point Entry", "sales_invoice"):
		return

	artech_engine.db.sql(
		"""UPDATE `tabLoyalty Point Entry` lpe
		SET lpe.`invoice_type` = 'Sales Invoice', lpe.`invoice` = lpe.`sales_invoice`
		WHERE lpe.`sales_invoice` IS NOT NULL
		AND (lpe.`invoice` IS NULL OR lpe.`invoice` = '')"""
	)
