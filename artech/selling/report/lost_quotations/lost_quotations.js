// Copyright (c) 2023, Artech and contributors

artech_engine.query_reports["Lost Quotations"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
		},
		{
			label: "Timespan",
			fieldtype: "Select",
			fieldname: "timespan",
			options: [
				"Last Week",
				"Last Month",
				"Last Quarter",
				"Last 6 months",
				"Last Year",
				"This Week",
				"This Month",
				"This Quarter",
				"This Year",
			],
			default: "This Year",
			reqd: 1,
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: ["Lost Reason", "Competitor"],
			default: "Lost Reason",
			reqd: 1,
		},
	],
};
