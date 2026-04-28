// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["BOM Explorer"] = {
	filters: [
		{
			fieldname: "bom",
			label: __("BOM"),
			fieldtype: "Link",
			options: "BOM",
			reqd: 1,
		},
	],
};
