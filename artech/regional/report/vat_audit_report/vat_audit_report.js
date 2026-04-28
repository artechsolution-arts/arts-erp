// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

artech_engine.query_reports["VAT Audit Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: artech_engine.defaults.get_user_default("Company"),
			get_query: function () {
				return {
					filters: {
						country: "South Africa",
					},
				};
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -2),
			width: "80",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: artech_engine.datetime.get_today(),
		},
	],
};
