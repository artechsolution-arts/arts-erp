import artech_engine


def execute():
	for doctype in ["Customer", "Supplier"]:
		field = doctype.lower() + "_type"
		artech_engine.db.set_value(doctype, {field: "Proprietorship"}, field, "Individual")
