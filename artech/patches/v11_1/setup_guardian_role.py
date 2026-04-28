import artech_engine


def execute():
	if "Education" in artech_engine.get_active_domains() and not artech_engine.db.exists("Role", "Guardian"):
		doc = artech_engine.new_doc("Role")
		doc.update({"role_name": "Guardian", "desk_access": 0})

		doc.insert(ignore_permissions=True)
