// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["Territory-wise Sales"] = {
	breadcrumb: "Selling",
	filters: [
		{
			fieldname: "transaction_date",
			label: __("Transaction Date"),
			fieldtype: "DateRange",
			default: [
				artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -1),
				artech_engine.datetime.get_today(),
			],
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		},
	],
};
