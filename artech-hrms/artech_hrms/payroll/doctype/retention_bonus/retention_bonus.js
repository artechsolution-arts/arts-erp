artech_engine.ui.form.on("Retention Bonus", {
	setup: function (frm) {
		frm.set_query("employee", function () {
			if (!frm.doc.company) {
				artech_engine.msgprint(__("Please Select Company First"));
			}
			return {
				filters: {
					status: "Active",
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("salary_component", function () {
			return {
				filters: {
					type: "Earning",
				},
			};
		});
	},

	employee: function (frm) {
		if (frm.doc.employee) {
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
		}
	},
});
