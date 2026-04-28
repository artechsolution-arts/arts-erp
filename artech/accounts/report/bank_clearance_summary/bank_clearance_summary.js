// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

artech_engine.query_reports["Bank Clearance Summary"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech.utils.get_fiscal_year(artech_engine.datetime.get_today(), true)[1],
			width: "80",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
		},
		{
			fieldname: "account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: "Account",
			reqd: 1,
			default: artech_engine.defaults.get_user_default("Company")
				? locals[":Company"][artech_engine.defaults.get_user_default("Company")]["default_bank_account"]
				: "",
			get_query: function () {
				return {
					query: "artech.controllers.queries.get_account_list",
					filters: [
						["Account", "account_type", "in", "Bank, Cash"],
						["Account", "is_group", "=", 0],
					],
				};
			},
		},
	],
};
