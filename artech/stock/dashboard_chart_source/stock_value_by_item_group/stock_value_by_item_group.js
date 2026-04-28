artech_engine.provide("artech_engine.dashboards.chart_sources");

artech_engine.dashboards.chart_sources["Stock Value by Item Group"] = {
	method: "artech.stock.dashboard_chart_source.stock_value_by_item_group.stock_value_by_item_group.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
			reqd: 1,
		},
	],
};
