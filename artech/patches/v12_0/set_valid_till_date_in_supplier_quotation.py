import artech_engine


def execute():
	artech_engine.reload_doc("buying", "doctype", "supplier_quotation")
	artech_engine.db.sql(
		"""UPDATE `tabSupplier Quotation`
		SET valid_till = DATE_ADD(transaction_date , INTERVAL 1 MONTH)
		WHERE docstatus < 2"""
	)
