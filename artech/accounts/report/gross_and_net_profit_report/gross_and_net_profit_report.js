artech_engine.query_reports["Gross and Net Profit Report"] = $.extend({}, artech.financial_statements);

artech_engine.query_reports["Gross and Net Profit Report"]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
});
