artech_engine.ui.form.on("Training Event", {
	onload_post_render: function (frm) {
		frm.get_field("employees").grid.set_multiple_add("employee");
	},
	refresh: function (frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Training Result"), function () {
				artech_engine.route_options = {
					training_event: frm.doc.name,
				};
				artech_engine.set_route("List", "Training Result");
			});
			frm.add_custom_button(__("Training Feedback"), function () {
				artech_engine.route_options = {
					training_event: frm.doc.name,
				};
				artech_engine.set_route("List", "Training Feedback");
			});
		}
		frm.events.set_employee_query(frm);
	},

	set_employee_query: function (frm) {
		let emp = [];
		for (let d in frm.doc.employees) {
			if (frm.doc.employees[d].employee) {
				emp.push(frm.doc.employees[d].employee);
			}
		}
		frm.set_query("employee", "employees", function () {
			return {
				filters: {
					name: ["NOT IN", emp],
					status: "Active",
				},
			};
		});
	},
});

artech_engine.ui.form.on("Training Event Employee", {
	employee: function (frm) {
		frm.events.set_employee_query(frm);
	},
});
