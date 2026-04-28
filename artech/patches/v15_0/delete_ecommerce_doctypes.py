import click
import artech_engine


def execute():
	if "webshop" in artech_engine.get_installed_apps():
		return

	if not artech_engine.db.table_exists("Website Item"):
		return

	doctypes = [
		"E Commerce Settings",
		"Website Item",
		"Recommended Items",
		"Item Review",
		"Wishlist Item",
		"Wishlist",
		"Website Offer",
		"Website Item Tabbed Section",
	]

	for doctype in doctypes:
		artech_engine.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"ECommerce is renamed and moved to a separate app"
		"Please install the app for ECommerce features: https://github.com/artech_engine/webshop",
		fg="yellow",
	)
