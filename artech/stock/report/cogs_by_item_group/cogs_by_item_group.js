artech_engine.query_reports["COGS By Item Group"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			mandatory: true,
			default: artech_engine.defaults.get_user_default("Company"),
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			mandatory: true,
			default: artech_engine.datetime.year_start(),
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			mandatory: true,
			default: artech_engine.datetime.get_today(),
		},
	],
};
