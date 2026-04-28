# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("artech_integrations", "doctype", "plaid_settings")
	plaid_settings = artech_engine.get_single("Plaid Settings")
	if plaid_settings.enabled:
		if not (artech_engine.conf.plaid_client_id and artech_engine.conf.plaid_env and artech_engine.conf.plaid_secret):
			plaid_settings.enabled = 0
		else:
			plaid_settings.update(
				{
					"plaid_client_id": artech_engine.conf.plaid_client_id,
					"plaid_env": artech_engine.conf.plaid_env,
					"plaid_secret": artech_engine.conf.plaid_secret,
				}
			)
		plaid_settings.flags.ignore_mandatory = True
		plaid_settings.save()
