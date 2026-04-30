artech_engine.ui.form.on("Attendance", {
	refresh(frm) {
		if (frm.doc.__islocal && !frm.doc.attendance_date) {
			frm.set_value("attendance_date", artech_engine.datetime.get_today());
		}

		frm.set_query("employee", () => {
			return {
				query: "artech.controllers.queries.employee_query",
			};
		});

		if (frm.doc.docstatus === 1 && frm.doc.status === "Absent") {
			frm.add_custom_button(
				__("Attendance Request"),
				() => {
					artech_engine.new_doc("Attendance Request", {
						employee: frm.doc.employee,
						from_date: frm.doc.attendance_date,
						to_date: frm.doc.attendance_date,
					});
				},
				__("Create"),
			);
		}
	},
});
