/* eslint-disable */

artech_engine.query_reports["Recruitment Analytics"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "on_date",
			label: __("On Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.now_date(),
			reqd: 1,
		},
	],
};
