import artech_engine


def execute():
	artech_engine.db.sql(
		"""
		update `tabMaterial Request`
		set status='Manufactured'
		where docstatus=1 and material_request_type='Manufacture' and per_ordered=100 and status != 'Stopped'
	"""
	)
