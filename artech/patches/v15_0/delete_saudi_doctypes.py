import click
import artech_engine


def execute():
	if "ksa" in artech_engine.get_installed_apps():
		return

	doctypes = ["KSA VAT Setting", "KSA VAT Purchase Account", "KSA VAT Sales Account"]
	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True)

	print_formats = ["KSA POS Invoice", "KSA VAT Invoice"]
	for print_format in print_formats:
		artech_engine.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = ["KSA VAT"]
	for report in reports:
		artech_engine.delete_doc("Report", report, ignore_missing=True, force=True)

	click.secho(
		"Region Saudi Arabia(KSA) is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/8848digital/KSA",
		fg="yellow",
	)
