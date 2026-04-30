import artech_engine

from artech_hrms.regional.india.setup import make_custom_fields


def execute():
	company = artech_engine.get_all("Company", filters={"country": "India"})
	if not company:
		return

	make_custom_fields()

	artech_engine.reload_doc("payroll", "doctype", "income_tax_slab")
