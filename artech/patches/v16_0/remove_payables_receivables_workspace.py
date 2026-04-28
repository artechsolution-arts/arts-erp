import artech_engine


def execute():
	for ws in ["Receivables", "Payables"]:
		artech_engine.delete_doc_if_exists("Workspace Sidebar", ws)
		artech_engine.delete_doc_if_exists("Workspace", ws)
