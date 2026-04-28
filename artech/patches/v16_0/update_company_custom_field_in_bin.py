import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "bin")

	artech_engine.db.sql(
		"""
        UPDATE `tabBin` b
        INNER JOIN `tabWarehouse` w ON b.warehouse = w.name
        SET b.company = w.company
        WHERE b.company IS NULL OR b.company = ''
    """
	)
