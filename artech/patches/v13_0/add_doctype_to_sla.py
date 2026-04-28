import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.reload_doc("support", "doctype", "sla_fulfilled_on_status")
	artech_engine.reload_doc("support", "doctype", "service_level_agreement")
	if artech_engine.db.has_column("Service Level Agreement", "enable"):
		rename_field("Service Level Agreement", "enable", "enabled")

	for sla in artech_engine.get_all("Service Level Agreement"):
		agreement = artech_engine.get_doc("Service Level Agreement", sla.name)
		agreement.db_set("document_type", "Issue")
		agreement.reload()
		agreement.apply_sla_for_resolution = 1
		agreement.append("sla_fulfilled_on", {"status": "Resolved"})
		agreement.append("sla_fulfilled_on", {"status": "Closed"})
		agreement.save()
