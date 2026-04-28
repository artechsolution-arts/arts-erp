# Copyright (c) 2021, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import artech_engine


# Patch kept for users outside India
def execute():
	if artech_engine.db.exists("Company", {"country": "India"}):
		return

	for field in (
		"gst_section",
		"company_address",
		"company_gstin",
		"place_of_supply",
		"customer_address",
		"customer_gstin",
	):
		artech_engine.delete_doc_if_exists("Custom Field", f"Payment Entry-{field}")
