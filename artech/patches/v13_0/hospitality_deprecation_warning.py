import click


def execute():
	click.secho(
		"Hospitality domain is moved to a separate app and will be removed from Artech in version-14.\n"
		"When upgrading to Artech version-14, please install the app to continue using the Hospitality domain: https://github.com/artech_engine/hospitality",
		fg="yellow",
	)
