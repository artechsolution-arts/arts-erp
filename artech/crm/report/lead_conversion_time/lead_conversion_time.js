// Copyright (c) 2018, Artech and contributors

artech_engine.query_reports["Lead Conversion Time"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: artech_engine.datetime.add_days(artech_engine.datetime.nowdate(), -30),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: artech_engine.datetime.nowdate(),
		},
	],
};
