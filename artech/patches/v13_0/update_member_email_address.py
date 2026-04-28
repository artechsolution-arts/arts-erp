# Copyright (c) 2020, Artech and Contributors
# MIT License. See license.txt


import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	"""add value to email_id column from email"""

	if artech_engine.db.has_column("Member", "email"):
		# Get all members
		for member in artech_engine.db.get_all("Member", pluck="name"):
			# Check if email_id already exists
			if not artech_engine.db.get_value("Member", member, "email_id"):
				# fetch email id from the user linked field email
				email = artech_engine.db.get_value("Member", member, "email")

				# Set the value for it
				artech_engine.db.set_value("Member", member, "email_id", email)

	if artech_engine.db.exists("DocType", "Membership Settings"):
		rename_field("Membership Settings", "enable_auto_invoicing", "enable_invoicing")
