artech_engine.query_reports["Vehicle Expenses"] = {
	filters: [
		{
			fieldname: "filter_based_on",
			label: __("Filter Based On"),
			fieldtype: "Select",
			options: ["Fiscal Year", "Date Range"],
			default: ["Fiscal Year"],
			reqd: 1,
			on_change: () => {
				let filter_based_on = artech_engine.query_report.get_filter_value("filter_based_on");

				if (filter_based_on == "Fiscal Year") {
					set_reqd_filter("fiscal_year", true);
					set_reqd_filter("from_date", false);
					set_reqd_filter("to_date", false);
				}
				if (filter_based_on == "Date Range") {
					set_reqd_filter("fiscal_year", false);
					set_reqd_filter("from_date", true);
					set_reqd_filter("to_date", true);
				}
			},
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: artech_engine.defaults.get_user_default("fiscal_year"),
			depends_on: "eval: doc.filter_based_on == 'Fiscal Year'",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			depends_on: "eval: doc.filter_based_on == 'Date Range'",
			default: artech_engine.datetime.add_months(artech_engine.datetime.nowdate(), -12),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			depends_on: "eval: doc.filter_based_on == 'Date Range'",
			default: artech_engine.datetime.nowdate(),
		},
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Vehicle",
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},
	],
};

function set_reqd_filter(fieldname, is_reqd) {
	let filter = artech_engine.query_report.get_filter(fieldname);
	filter.df.reqd = is_reqd;
	filter.refresh();
}
