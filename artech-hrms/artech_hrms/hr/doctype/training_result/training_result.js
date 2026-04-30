artech_engine.ui.form.on("Training Result", {
	training_event: function (frm) {
		if (frm.doc.training_event && !frm.doc.docstatus) {
			artech_engine.call({
				method: "hrms.hr.doctype.training_result.training_result.get_employees",
				args: {
					training_event: frm.doc.training_event,
				},
				callback: function (r) {
					frm.set_value("employees", "");
					if (r.message) {
						$.each(r.message, function (i, d) {
							var row = artech_engine.model.add_child(
								frm.doc,
								"Training Result Employee",
								"employees",
							);
							row.employee = d.employee;
							row.employee_name = d.employee_name;
						});
					}
					refresh_field("employees");
				},
			});
		}
	},
});
