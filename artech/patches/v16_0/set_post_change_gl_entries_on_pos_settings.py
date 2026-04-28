import artech_engine


def execute():
	Singles = artech_engine.qb.DocType("Singles")
	query = (
		artech_engine.qb.from_(Singles)
		.select("value")
		.where((Singles.doctype == "Accounts Settings") & (Singles.field == "post_change_gl_entries"))
	)
	result = query.run(as_dict=1)
	if result:
		post_change_gl_entries = int(result[0].get("value", 1))
		artech_engine.db.set_single_value("POS Settings", "post_change_gl_entries", post_change_gl_entries)
