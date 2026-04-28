import click
import artech_engine


def execute():
	if "lending" in artech_engine.get_installed_apps():
		return

	click.secho(
		"Loan Management module has been moved to a separate app"
		" and will be removed from Artech in Version 15."
		" Please install the Lending app when upgrading to Version 15"
		" to continue using the Loan Management module:\n"
		"https://github.com/artech_engine/lending",
		fg="yellow",
	)
