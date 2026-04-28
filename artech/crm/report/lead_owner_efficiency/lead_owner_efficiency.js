// Copyright (c) 2016, Artech and contributors
artech_engine.query_reports["Lead Owner Efficiency"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech.utils.get_fiscal_year(artech_engine.datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech.utils.get_fiscal_year(artech_engine.datetime.get_today(), true)[2],
		},
	],
};
