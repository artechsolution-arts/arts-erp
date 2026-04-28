import artech_engine


def execute():
	artech_engine.reload_doc("core", "doctype", "scheduled_job_type")
	if artech_engine.db.exists("Scheduled Job Type", "repost_item_valuation.repost_entries"):
		artech_engine.db.set_value("Scheduled Job Type", "repost_item_valuation.repost_entries", "stopped", 0)
