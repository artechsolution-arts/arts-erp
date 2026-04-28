import artech_engine


def execute():
	recoverable = ("QueryDeadlockError", "QueryTimeoutError", "JobTimeoutException")

	failed_reposts = artech_engine.get_all(
		"Repost Item Valuation",
		fields=["name", "error_log"],
		filters={
			"status": "Failed",
			"docstatus": 1,
			"modified": (">", "2022-04-20"),
			"error_log": ("is", "set"),
		},
	)
	for riv in failed_reposts:
		for exc in recoverable:
			if exc in riv.error_log:
				artech_engine.db.set_value("Repost Item Valuation", riv.name, "status", "Queued")
				break
