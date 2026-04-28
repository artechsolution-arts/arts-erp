import artech_engine


def execute():
	for ws in ["Retail", "Utilities"]:
		artech_engine.delete_doc_if_exists("Workspace", ws)

	for ws in ["Integrations", "Settings"]:
		artech_engine.db.set_value("Workspace", ws, "public", 0)
