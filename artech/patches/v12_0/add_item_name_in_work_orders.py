import artech_engine


def execute():
	artech_engine.reload_doc("manufacturing", "doctype", "work_order")

	artech_engine.db.sql(
		"""
		UPDATE
			`tabWork Order` wo
				JOIN `tabItem` item ON wo.production_item = item.item_code
		SET
			wo.item_name = item.item_name
	"""
	)
	artech_engine.db.commit()
