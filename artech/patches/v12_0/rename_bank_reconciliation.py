# Copyright (c) 2018, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	if artech_engine.db.table_exists("Bank Reconciliation"):
		artech_engine.rename_doc("DocType", "Bank Reconciliation", "Bank Clearance", force=True)
		artech_engine.reload_doc("Accounts", "doctype", "Bank Clearance")

		artech_engine.rename_doc("DocType", "Bank Reconciliation Detail", "Bank Clearance Detail", force=True)
		artech_engine.reload_doc("Accounts", "doctype", "Bank Clearance Detail")
