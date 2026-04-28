// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["Downtime Analysis"] = {
	filters: [
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Datetime",
			default: artech_engine.datetime.convert_to_system_tz(
				artech_engine.datetime.add_months(artech_engine.datetime.now_datetime(), -1)
			),
			reqd: 1,
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Datetime",
			default: artech_engine.datetime.now_datetime(),
			reqd: 1,
		},
		{
			label: __("Machine"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation",
		},
	],
};
