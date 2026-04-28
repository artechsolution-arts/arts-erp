import artech_engine


def execute():
	artech_engine.reload_doc("manufacturing", "doctype", "bom_operation")
	artech_engine.reload_doc("manufacturing", "doctype", "work_order_operation")

	artech_engine.db.sql(
		"""
        UPDATE
            `tabBOM Operation` bo
        SET
            bo.batch_size = 1
    """
	)
	artech_engine.db.sql(
		"""
        UPDATE
            `tabWork Order Operation` wop
        SET
            wop.batch_size = 1
    """
	)
