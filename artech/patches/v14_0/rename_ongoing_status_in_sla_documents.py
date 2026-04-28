import artech_engine


def execute():
	active_sla_documents = [
		sla.document_type for sla in artech_engine.get_all("Service Level Agreement", fields=["document_type"])
	]

	for doctype in active_sla_documents:
		doctype = artech_engine.qb.DocType(doctype)
		try:
			artech_engine.qb.update(doctype).set(doctype.agreement_status, "First Response Due").where(
				doctype.first_responded_on.isnull()
			).run()

			artech_engine.qb.update(doctype).set(doctype.agreement_status, "Resolution Due").where(
				doctype.agreement_status == "Ongoing"
			).run()

		except Exception:
			artech_engine.log_error("Failed to Patch SLA Status")
