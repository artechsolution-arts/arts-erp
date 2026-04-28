// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["YouTube Interactions"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.add_months(artech_engine.datetime.now_date(), -12),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.now_date(),
		},
	],
};
