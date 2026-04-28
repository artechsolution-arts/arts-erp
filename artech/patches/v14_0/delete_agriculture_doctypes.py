import artech_engine


def execute():
	if "agriculture" in artech_engine.get_installed_apps():
		return

	artech_engine.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)

	artech_engine.delete_doc("Workspace", "Agriculture", ignore_missing=True, force=True)

	reports = artech_engine.get_all("Report", {"module": "agriculture", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		artech_engine.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = artech_engine.get_all("Dashboard", {"module": "agriculture", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		artech_engine.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = artech_engine.get_all("DocType", {"module": "agriculture", "custom": 0}, pluck="name")
	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True)

	artech_engine.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)
