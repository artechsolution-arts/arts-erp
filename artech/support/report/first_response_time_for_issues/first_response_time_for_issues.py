# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import artech_engine
from artech_engine import _


def execute(filters=None):
	columns = [
		{"fieldname": "creation_date", "label": _("Date"), "fieldtype": "Date", "width": 300},
		{
			"fieldname": "first_response_time",
			"fieldtype": "Duration",
			"label": _("First Response Time"),
			"width": 300,
		},
	]

	data = artech_engine.db.sql(
		"""
		SELECT
			date(creation) as creation_date,
			avg(first_response_time) as avg_response_time
		FROM tabIssue
		WHERE
			date(creation) between %s and %s
			and first_response_time > 0
		GROUP BY creation_date
		ORDER BY creation_date desc
	""",
		(filters.from_date, filters.to_date),
	)

	return columns, data
