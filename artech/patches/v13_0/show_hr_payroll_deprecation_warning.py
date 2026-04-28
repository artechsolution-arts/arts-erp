import click
import artech_engine


def execute():
	if "hrms" in artech_engine.get_installed_apps():
		return

	click.secho(
		"HR and Payroll modules have been moved to a separate app"
		" and will be removed from Artech in Version 14."
		" Please install the HRMS app when upgrading to Version 14"
		" to continue using the HR and Payroll modules:\n"
		"https://github.com/artech_engine/hrms",
		fg="yellow",
	)
