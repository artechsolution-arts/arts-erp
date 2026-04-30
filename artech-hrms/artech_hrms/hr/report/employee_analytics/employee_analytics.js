/* eslint-disable */

artech_engine.query_reports["Employee Analytics"] = {
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
			fieldname: "parameter",
			label: __("Parameter"),
			fieldtype: "Select",
			options: ["Branch", "Grade", "Department", "Designation", "Employment Type"],
			reqd: 1,
		},
	],
};
