artech_engine.provide("artech_engine.dashboards.chart_sources");

artech_engine.dashboards.chart_sources["Employees by Age"] = {
	method: "hrms.hr.dashboard_chart_source.employees_by_age.employees_by_age.get_data",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
		},
	],
};
