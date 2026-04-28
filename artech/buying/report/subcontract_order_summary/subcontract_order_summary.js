// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["Subcontract Order Summary"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
			reqd: 1,
		},
		{
			label: __("Order Type"),
			fieldname: "order_type",
			fieldtype: "Select",
			options: ["Purchase Order", "Subcontracting Order"],
			default: "Subcontracting Order",
		},
		{
			label: __("Subcontract Order"),
			fieldname: "name",
			fieldtype: "Data",
		},
	],
};
