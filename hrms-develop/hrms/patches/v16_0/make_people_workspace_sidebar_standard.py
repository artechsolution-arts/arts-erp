import artech_engine


def execute():
	if artech_engine.db.table_exists("Workspace Sidebar"):
		if artech_engine.db.exists("Workspace Sidebar", "People"):
			artech_engine.db.set_value("Workspace Sidebar", "People", "standard", 1)
