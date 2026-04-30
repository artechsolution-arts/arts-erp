artech_engine.query_reports["Employee Leave Balance"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
		},
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: artech_engine.defaults.get_user_default("Company"),
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},
		{
			fieldname: "employee_status",
			label: __("Employee Status"),
			fieldtype: "Select",
			options: [
				"",
				{ value: "Active", label: __("Active") },
				{ value: "Inactive", label: __("Inactive") },
				{ value: "Suspended", label: __("Suspended") },
				{ value: "Left", label: __("Left", null, "Employee") },
			],
			default: "Active",
		},
		{
			fieldname: "consolidate_leave_types",
			label: __("Consolidate Leave Types"),
			fieldtype: "Check",
			default: 1,
			depends_on: "eval: !doc.employee",
		},
	],
	onload: () => {
		const today = artech_engine.datetime.now_date();

		artech_engine.call({
			type: "GET",
			method: "artech_hrms.hr.utils.get_leave_period",
			args: {
				from_date: today,
				to_date: today,
				company: artech_engine.defaults.get_user_default("Company"),
			},
			freeze: true,
			callback: (data) => {
				artech_engine.query_report.set_filter_value("from_date", data.message[0].from_date);
				artech_engine.query_report.set_filter_value("to_date", data.message[0].to_date);
			},
		});
	},
};
