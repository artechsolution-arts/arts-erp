import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "pick_list")
	artech_engine.db.sql(
		"""UPDATE `tabPick List` set purpose = 'Delivery'
        WHERE docstatus = 1  and purpose = 'Delivery against Sales Order' """
	)
