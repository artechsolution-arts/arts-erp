# Copyright (c) 2015, Artech and Contributors


import artech_engine


def execute():
	for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
		if artech_engine.db.exists("Report", report):
			artech_engine.delete_doc("Report", report)
