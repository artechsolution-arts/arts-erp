// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

artech_engine.query_reports["Support Hour Distribution"] = {
	filters: [
		{
			lable: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: artech_engine.datetime.nowdate(),
			reqd: 1,
		},
		{
			lable: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: artech_engine.datetime.nowdate(),
			reqd: 1,
		},
	],
};
