# Copyright (c) 2020, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	if artech_engine.db.exists("DocType", "Issue"):
		artech_engine.reload_doc("support", "doctype", "issue")
		rename_status()


def rename_status():
	artech_engine.db.sql(
		"""
		UPDATE
			`tabIssue`
		SET
			status = 'On Hold'
		WHERE
			status = 'Hold'
	"""
	)
