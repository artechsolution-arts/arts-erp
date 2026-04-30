artech_engine.ui.form.on("Shift Schedule", {
	refresh(frm) {
		if (frm.doc.docstatus === 1)
			artech_hrms.add_shift_tools_button_to_form(frm, {
				action: "Assign Shift Schedule",
				shift_schedule: frm.doc.name,
			});
	},
});
