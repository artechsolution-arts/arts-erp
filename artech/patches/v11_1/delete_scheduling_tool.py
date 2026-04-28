# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	if artech_engine.db.exists("DocType", "Scheduling Tool"):
		artech_engine.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
