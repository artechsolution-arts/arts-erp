artech_engine.query_reports["Accrued Earnings Report"] = {
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
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			get_query: function () {
				let company = artech_engine.query_report.get_filter_value("company");
				let department = artech_engine.query_report.get_filter_value("department");
				let branch = artech_engine.query_report.get_filter_value("branch");

				let filters = {};
				if (company) {
					filters["company"] = company;
				}
				if (department) {
					filters["department"] = department;
				}
				if (branch) {
					filters["branch"] = branch;
				}

				return {
					filters: filters,
				};
			},
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
			get_query: function () {
				let company = artech_engine.query_report.get_filter_value("company");
				return {
					filters: {
						company: company,
					},
				};
			},
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "payroll_period",
			label: __("Payroll Period"),
			fieldtype: "Link",
			options: "Payroll Period",
			reqd: 1,
			get_query: function () {
				let company = artech_engine.query_report.get_filter_value("company");
				return {
					filters: {
						company: company,
					},
				};
			},
		},
		{
			fieldname: "salary_component",
			label: __("Salary Component"),
			fieldtype: "Link",
			options: "Salary Component",
			get_query: function () {
				return {
					filters: {
						accrual_component: 1,
					},
				};
			},
		},
		{
			fieldname: "flexible_benefit",
			label: __("Flexible Benefit"),
			fieldtype: "Select",
			options: "\nYes\nNo",
			default: "",
		},
	],
};

// To create additional salary with pre-populated fields
function create_additional_salary(employee, salary_component, amount) {
	let company = artech_engine.query_report.get_filter_value("company");

	const doc = artech_engine.model.get_new_doc("Additional Salary");
	doc.company = company;
	doc.employee = employee;
	doc.salary_component = salary_component;
	doc.type = "Earning";
	doc.is_recurring = 0;
	doc.payroll_date = artech_engine.datetime.get_today();
	doc.amount = amount;
	doc.overwrite_salary_structure_amount = 0;
	doc.ref_doctype = "Employee Benefit Ledger";
	artech_engine.set_route("Form", "Additional Salary", doc.name);
}
