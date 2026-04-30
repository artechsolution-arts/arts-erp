import artech_engine


@artech_engine.whitelist()
def get_assignment_rules_list():
	assignment_rules = []
	for docname in artech_engine.get_all(
		"Assignment Rule", filters={"document_type": ["in", ["CRM Lead", "CRM Deal"]]}
	):
		doc = artech_engine.get_value(
			"Assignment Rule",
			docname,
			fieldname=[
				"name",
				"description",
				"disabled",
				"priority",
			],
			as_dict=True,
		)
		users_exists = bool(artech_engine.db.exists("Assignment Rule User", {"parent": docname.name}))
		assignment_rules.append({**doc, "users_exists": users_exists})
	return assignment_rules


@artech_engine.whitelist()
def duplicate_assignment_rule(docname: str, new_name: str):
	doc = artech_engine.get_doc("Assignment Rule", docname)
	doc.name = new_name
	doc.assignment_rule_name = new_name
	doc.insert()
	return doc
