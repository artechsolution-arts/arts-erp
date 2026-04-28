// Copyright (c) 2019, Artech and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Appointment", {
	refresh: function (frm) {
		if (frm.doc.lead) {
			frm.add_custom_button(frm.doc.lead, () => {
				artech_engine.set_route("Form", "Lead", frm.doc.lead);
			});
		}
		if (frm.doc.calendar_event) {
			frm.add_custom_button(__(frm.doc.calendar_event), () => {
				artech_engine.set_route("Form", "Event", frm.doc.calendar_event);
			});
		}
	},
	onload: function (frm) {
		frm.set_query("appointment_with", function () {
			return {
				filters: {
					name: ["in", ["Customer", "Lead"]],
				},
			};
		});
	},
});
