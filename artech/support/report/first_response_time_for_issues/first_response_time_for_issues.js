// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

artech_engine.query_reports["First Response Time for Issues"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: artech_engine.datetime.add_days(artech_engine.datetime.nowdate(), -30),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: artech_engine.datetime.nowdate(),
		},
	],
	get_chart_data: function (_columns, result) {
		return {
			data: {
				labels: result.map((d) => d.creation_date),
				datasets: [
					{
						name: "First Response Time",
						values: result.map((d) => d.first_response_time),
					},
				],
			},
			type: "line",
			tooltipOptions: {
				formatTooltipY: (d) => {
					let duration_options = {
						hide_days: 0,
						hide_seconds: 0,
					};
					return artech_engine.utils.get_formatted_duration(d, duration_options);
				},
			},
		};
	},
};
