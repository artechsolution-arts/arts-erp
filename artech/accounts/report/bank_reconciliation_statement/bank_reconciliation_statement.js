// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

artech_engine.query_reports["Bank Reconciliation Statement"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: artech_engine.defaults.get_user_default("Company"),
		},
		{
			fieldname: "account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: "Account",
			default: artech_engine.defaults.get_user_default("Company")
				? locals[":Company"][artech_engine.defaults.get_user_default("Company")]["default_bank_account"]
				: "",
			reqd: 1,
			get_query: function () {
				var company = artech_engine.query_report.get_filter_value("company");
				return {
					query: "artech.controllers.queries.get_account_list",
					filters: [
						["Account", "account_type", "in", "Bank, Cash"],
						["Account", "is_group", "=", 0],
						["Account", "disabled", "=", 0],
						["Account", "company", "=", company],
					],
				};
			},
		},
		{
			fieldname: "report_date",
			label: __("Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "include_pos_transactions",
			label: __("Include POS Transactions"),
			fieldtype: "Check",
		},
	],
	formatter: function (value, row, column, data, default_formatter, filter) {
		if (column.fieldname == "payment_entry" && value == __("Cheques and Deposits incorrectly cleared")) {
			column.link_onclick =
				"artech_engine.query_reports['Bank Reconciliation Statement'].open_utility_report()";
		}
		return default_formatter(value, row, column, data);
	},
	open_utility_report: function () {
		artech_engine.route_options = {
			company: artech_engine.query_report.get_filter_value("company"),
			account: artech_engine.query_report.get_filter_value("account"),
			report_date: artech_engine.query_report.get_filter_value("report_date"),
		};
		artech_engine.open_in_new_tab = true;
		artech_engine.set_route("query-report", "Cheques and Deposits Incorrectly cleared");
	},
};
