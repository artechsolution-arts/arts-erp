# Copyright (c) 2013, Artech and contributors
# For license information, please see license.txt


from artech.selling.report.sales_analytics.sales_analytics import Analytics


def execute(filters=None):
	return Analytics(filters).run()
