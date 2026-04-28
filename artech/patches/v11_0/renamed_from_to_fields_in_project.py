# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.reload_doc("projects", "doctype", "project")

	if artech_engine.db.has_column("Project", "from"):
		rename_field("Project", "from", "from_time")
		rename_field("Project", "to", "to_time")
