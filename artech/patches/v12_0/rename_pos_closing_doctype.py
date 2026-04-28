# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	if artech_engine.db.table_exists("POS Closing Voucher"):
		if not artech_engine.db.exists("DocType", "POS Closing Entry"):
			artech_engine.rename_doc("DocType", "POS Closing Voucher", "POS Closing Entry", force=True)

		if not artech_engine.db.exists("DocType", "POS Closing Entry Taxes"):
			artech_engine.rename_doc("DocType", "POS Closing Voucher Taxes", "POS Closing Entry Taxes", force=True)

		if not artech_engine.db.exists("DocType", "POS Closing Voucher Details"):
			artech_engine.rename_doc(
				"DocType", "POS Closing Voucher Details", "POS Closing Entry Detail", force=True
			)

		artech_engine.reload_doc("Accounts", "doctype", "POS Closing Entry")
		artech_engine.reload_doc("Accounts", "doctype", "POS Closing Entry Taxes")
		artech_engine.reload_doc("Accounts", "doctype", "POS Closing Entry Detail")

	if artech_engine.db.exists("DocType", "POS Closing Voucher"):
		artech_engine.delete_doc("DocType", "POS Closing Voucher")
		artech_engine.delete_doc("DocType", "POS Closing Voucher Taxes")
		artech_engine.delete_doc("DocType", "POS Closing Voucher Details")
		artech_engine.delete_doc("DocType", "POS Closing Voucher Invoices")
