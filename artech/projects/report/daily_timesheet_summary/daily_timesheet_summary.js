// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["Daily Timesheet Summary"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
		},
	],
};
