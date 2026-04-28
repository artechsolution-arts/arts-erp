artech_engine.query_reports["Electronic Invoice Register"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -1),
			width: "80",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
		},
	],
	onload: function (reportview) {
		reportview.page.add_inner_button(__("Export E-Invoices"), function () {
			//TODO: refactor condition to disallow export if report has no data.
			if (!reportview.data.length) {
				artech_engine.msgprint(__("No data to export"));
				return;
			}

			var w = window.open(
				artech_engine.urllib.get_full_url(
					"/api/method/artech.regional.italy.utils.export_invoices?" +
						"filters=" +
						JSON.stringify(reportview.get_filter_values())
				)
			);
			if (!w) {
				artech_engine.msgprint(__("Please enable pop-ups"));
				return;
			}
		});
	},
};
