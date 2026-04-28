import click


def execute():
	click.secho(
		"Shopify Integration is moved to a separate app and will be removed from Artech in version-14.\n"
		"Please install the app to continue using the integration: https://github.com/artech_engine/ecommerce_integrations",
		fg="yellow",
	)
