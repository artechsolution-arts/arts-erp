// Copyright (c) 2018, Artech and Contributors
// MIT License. See license.txt
artech_engine.provide("artech_engine.desk");

artech_engine.ui.form.on("Event", {
	refresh: function (frm) {
		frm.set_query("reference_doctype", "event_participants", function () {
			return {
				filters: {
					name: ["in", ["Contact", "Lead", "Customer", "Supplier", "Employee", "Sales Partner"]],
				},
			};
		});

		frm.add_custom_button(
			__("Add Leads"),
			function () {
				new artech_engine.desk.eventParticipants(frm, "Lead");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Customers"),
			function () {
				new artech_engine.desk.eventParticipants(frm, "Customer");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Suppliers"),
			function () {
				new artech_engine.desk.eventParticipants(frm, "Supplier");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Employees"),
			function () {
				new artech_engine.desk.eventParticipants(frm, "Employee");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Sales Partners"),
			function () {
				new artech_engine.desk.eventParticipants(frm, "Sales Partner");
			},
			__("Add Participants")
		);
	},
});
