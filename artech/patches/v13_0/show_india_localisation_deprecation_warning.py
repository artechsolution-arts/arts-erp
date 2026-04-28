import click
import artech_engine


def execute():
	if (
		not artech_engine.db.exists("Company", {"country": "India"})
		or "india_compliance" in artech_engine.get_installed_apps()
	):
		return

	click.secho(
		"India-specific regional features have been moved to a separate app"
		" and will be removed from Artech in Version 14."
		" Please install India Compliance after upgrading to Version 14:\n"
		"https://github.com/resilient-tech/india-compliance",
		fg="yellow",
	)
