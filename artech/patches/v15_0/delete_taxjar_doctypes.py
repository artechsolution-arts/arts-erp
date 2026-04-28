import click
import artech_engine


def execute():
	if "taxjar_integration" in artech_engine.get_installed_apps():
		return

	doctypes = ["TaxJar Settings", "TaxJar Nexus", "Product Tax Category"]
	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"Taxjar Integration is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/artech_engine/taxjar_integration",
		fg="yellow",
	)
