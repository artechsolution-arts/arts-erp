// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["Subcontracted Item To Be Received"] = {
	filters: [
		{
			label: __("Order Type"),
			fieldname: "order_type",
			fieldtype: "Select",
			options: ["Purchase Order", "Subcontracting Order"],
			default: "Subcontracting Order",
		},
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
			reqd: 1,
		},
	],
};
