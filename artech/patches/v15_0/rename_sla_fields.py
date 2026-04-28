import artech_engine
from artech_engine.custom.doctype.custom_field.custom_field import rename_fieldname
from artech_engine.model.utils.rename_field import rename_field


def execute():
	doctypes = artech_engine.get_all("Service Level Agreement", pluck="document_type", distinct=True)
	for doctype in doctypes:
		if doctype == "Issue":
			continue

		if artech_engine.db.exists(
			"Custom Field", {"name": doctype + "-resolution_by", "fieldname": "resolution_by"}
		):
			rename_fieldname(doctype + "-resolution_by", "sla_resolution_by")

		if artech_engine.db.exists(
			"Custom Field", {"name": doctype + "-resolution_date", "fieldname": "resolution_date"}
		):
			rename_fieldname(doctype + "-resolution_date", "sla_resolution_date")

	rename_field("Issue", "resolution_by", "sla_resolution_by")
	rename_field("Issue", "resolution_date", "sla_resolution_date")
