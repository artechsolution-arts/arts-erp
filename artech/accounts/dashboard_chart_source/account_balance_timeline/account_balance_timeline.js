artech_engine.provide("artech_engine.dashboards.chart_sources");

artech_engine.dashboards.chart_sources["Account Balance Timeline"] = {
	method: "artech.accounts.dashboard_chart_source.account_balance_timeline.account_balance_timeline.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "Link",
			options: "Account",
			reqd: 1,
			default: locals[":Company"][artech_engine.defaults.get_user_default("Company")]["default_bank_account"],
			get_query: () => {
				return {
					filters: {
						account_type: "Bank",
						is_group: 0,
					},
				};
			},
		},
	],
};
