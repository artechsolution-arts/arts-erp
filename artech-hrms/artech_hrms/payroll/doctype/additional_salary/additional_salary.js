artech_engine.ui.form.on("Additional Salary", {
	setup: function (frm) {
		frm.add_fetch(
			"salary_component",
			"deduct_full_tax_on_selected_payroll_date",
			"deduct_full_tax_on_selected_payroll_date",
		);

		frm.set_query("employee", function () {
			return {
				filters: {
					company: frm.doc.company,
					status: ["!=", "Inactive"],
				},
			};
		});
	},

	onload: function (frm) {
		frm.trigger("set_component_query");
	},

	employee: function (frm) {
		if (frm.doc.employee) {
			artech_engine.run_serially([
				() => frm.trigger("get_employee_currency"),
				() => frm.trigger("set_company"),
			]);
		} else {
			frm.set_value("company", null);
		}
	},

	set_company: function (frm) {
		artech_engine.call({
			method: "artech_engine.client.get_value",
			args: {
				doctype: "Employee",
				fieldname: "company",
				filters: {
					name: frm.doc.employee,
				},
			},
			callback: function (data) {
				if (data.message) {
					frm.set_value("company", data.message.company);
				}
			},
		});
	},

	company: function (frm) {
		frm.trigger("set_component_query");
	},

	set_component_query: function (frm) {
		if (!frm.doc.company) return;

		frm.set_query("salary_component", function () {
			return {
				filters: {
					disabled: 0,
				},
			};
		});
	},

	get_employee_currency: function (frm) {
		artech_engine.call({
			method: "artech_hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment.get_employee_currency",
			args: {
				employee: frm.doc.employee,
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value("currency", r.message);
					frm.refresh_fields();
				}
			},
		});
	},

	salary_component: function (frm) {
		if (!frm.doc.ref_doctype) {
			frm.trigger("get_salary_component_amount");
		}
	},

	get_salary_component_amount: function (frm) {
		artech_engine.call({
			method: "artech_engine.client.get_value",
			args: {
				doctype: "Salary Component",
				fieldname: "amount",
				filters: {
					name: frm.doc.salary_component,
				},
			},
			callback: function (data) {
				if (data.message) {
					frm.set_value("amount", data.message.amount);
				}
			},
		});
	},
});
