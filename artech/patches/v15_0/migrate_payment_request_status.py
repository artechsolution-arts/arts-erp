import artech_engine


def execute():
	"""
	Description:
	Change Inward Payment Requests from statut 'Initiated' to correct status 'Requested'.
	Status 'Initiated' is reserved for Outward Payment Requests and was a semantic error in previour versions.
	"""
	so = artech_engine.qb.DocType("Payment Request")
	artech_engine.qb.update(so).set(so.status, "Requested").where(so.payment_request_type == "Inward").where(
		so.status == "Initiated"
	).run()
