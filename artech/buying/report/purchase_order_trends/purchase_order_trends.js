// Copyright (c) 2015, Artech and Contributors

artech_engine.query_reports["Purchase Order Trends"] = $.extend({}, artech.purchase_trends_filters);

artech_engine.query_reports["Purchase Order Trends"]["filters"].push({
	fieldname: "include_closed_orders",
	label: __("Include Closed Orders"),
	fieldtype: "Check",
	default: 0,
});
