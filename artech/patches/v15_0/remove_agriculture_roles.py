import artech_engine


def execute():
	if "agriculture" in artech_engine.get_installed_apps():
		return

	for role in ["Agriculture User", "Agriculture Manager"]:
		assignments = artech_engine.get_all("Has Role", {"role": role}, pluck="name")
		for assignment in assignments:
			artech_engine.delete_doc("Has Role", assignment, ignore_missing=True, force=True)
		artech_engine.delete_doc("Role", role, ignore_missing=True, force=True)
