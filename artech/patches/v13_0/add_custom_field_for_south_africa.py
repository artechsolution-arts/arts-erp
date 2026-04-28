import artech_engine

from artech.regional.south_africa.setup import add_permissions, make_custom_fields


def execute():
	company = artech_engine.get_all("Company", filters={"country": "South Africa"})
	if not company:
		return

	artech_engine.reload_doc("regional", "doctype", "south_africa_vat_settings")
	artech_engine.reload_doc("regional", "report", "vat_audit_report")
	artech_engine.reload_doc("accounts", "doctype", "south_africa_vat_account")

	make_custom_fields()
	add_permissions()
