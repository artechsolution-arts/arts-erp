import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.reload_doc("setup", "doctype", "company")
	if artech_engine.db.has_column("Company", "default_terms"):
		rename_field("Company", "default_terms", "default_selling_terms")

		for company in artech_engine.get_all("Company", ["name", "default_selling_terms", "default_buying_terms"]):
			if company.default_selling_terms and not company.default_buying_terms:
				artech_engine.db.set_value(
					"Company", company.name, "default_buying_terms", company.default_selling_terms
				)

	artech_engine.reload_doc("setup", "doctype", "terms_and_conditions")
	artech_engine.db.sql("update `tabTerms and Conditions` set selling=1, buying=1, hr=1")
