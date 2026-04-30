# MIT License. See license.txt
import click
import artech_engine


def before_uninstall():
	delete_email_template_custom_fields()


def delete_email_template_custom_fields():
	if artech_engine.get_meta("Email Template").has_field("enabled"):
		click.secho("* Uninstalling Custom Fields from Email Template")

		fieldnames = (
			"enabled",
			"reference_doctype",
		)

		for fieldname in fieldnames:
			artech_engine.db.delete("Custom Field", {"name": "Email Template-" + fieldname})

		artech_engine.clear_cache(doctype="Email Template")
