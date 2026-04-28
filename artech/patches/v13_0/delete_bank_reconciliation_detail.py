import artech_engine


def execute():
	if artech_engine.db.exists("DocType", "Bank Reconciliation Detail") and artech_engine.db.exists(
		"DocType", "Bank Clearance Detail"
	):
		artech_engine.delete_doc("DocType", "Bank Reconciliation Detail", force=1)
