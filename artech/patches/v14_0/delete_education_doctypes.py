import click
import artech_engine


def execute():
	if "education" in artech_engine.get_installed_apps():
		return

	artech_engine.delete_doc("Workspace", "Education", ignore_missing=True, force=True)

	pages = artech_engine.get_all("Page", {"module": "education"}, pluck="name")
	for page in pages:
		artech_engine.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = artech_engine.get_all("Report", {"module": "education", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		artech_engine.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = artech_engine.get_all("Print Format", {"module": "education", "standard": "Yes"}, pluck="name")
	for print_format in print_formats:
		artech_engine.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	artech_engine.reload_doc("website", "doctype", "website_settings")
	forms = artech_engine.get_all("Web Form", {"module": "education", "is_standard": 1}, pluck="name")
	for form in forms:
		artech_engine.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = artech_engine.get_all("Dashboard", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		artech_engine.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = artech_engine.get_all("Dashboard Chart", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		artech_engine.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	artech_engine.reload_doc("desk", "doctype", "number_card")
	cards = artech_engine.get_all("Number Card", {"module": "education", "is_standard": 1}, pluck="name")
	for card in cards:
		artech_engine.delete_doc("Number Card", card, ignore_missing=True, force=True)

	doctypes = artech_engine.get_all("DocType", {"module": "education", "custom": 0}, pluck="name")

	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True)

	titles = [
		"Fees",
		"Student Admission",
		"Grant Application",
		"Chapter",
		"Certification Application",
	]
	items = artech_engine.get_all("Portal Menu Item", filters=[["title", "in", titles]], pluck="name")
	for item in items:
		artech_engine.delete_doc("Portal Menu Item", item, ignore_missing=True, force=True)

	artech_engine.delete_doc("Module Def", "Education", ignore_missing=True, force=True)

	click.secho(
		"Education Module is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/artech_engine/education",
		fg="yellow",
	)
