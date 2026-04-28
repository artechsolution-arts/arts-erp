# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

import artech_engine


def execute():
	accounts_settings = artech_engine.get_doc("Accounts Settings", "Accounts Settings")
	accounts_settings.book_deferred_entries_based_on = "Days"
	accounts_settings.book_deferred_entries_via_journal_entry = 0
	accounts_settings.submit_journal_entries = 0
	accounts_settings.save()
