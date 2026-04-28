artech_engine.provide("artech_engine.dashboards.chart_sources");

artech_engine.dashboards.chart_sources["Warehouse wise Stock Value"] = {
	method: "artech.stock.dashboard_chart_source.warehouse_wise_stock_value.warehouse_wise_stock_value.get",
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
