import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "shipment")

	# update submitted status
	artech_engine.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Submitted"
					WHERE status = "Draft" AND docstatus = 1"""
	)

	# update cancelled status
	artech_engine.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Cancelled"
					WHERE status = "Draft" AND docstatus = 2"""
	)
