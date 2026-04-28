// Copyright (c) 2019, Artech and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Project Template", {
	// refresh: function(frm) {

	// }
	setup: function (frm) {
		frm.set_query("task", "tasks", function () {
			return {
				filters: {
					is_template: 1,
				},
			};
		});
	},
});

artech_engine.ui.form.on("Project Template Task", {
	task: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];

		if (!row.task) {
			row.subject = null;
			refresh_field("tasks");
			return;
		}

		artech_engine.db.get_value("Task", row.task, "subject", (value) => {
			row.subject = value.subject;
			refresh_field("tasks");
		});
	},
});
