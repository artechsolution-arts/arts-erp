// Copyright (c) 2021, Artech and contributors

artech_engine.ui.form.on("Prospect", {
	refresh(frm) {
		if (!frm.is_new() && artech_engine.boot.user.can_create.includes("Customer")) {
			frm.add_custom_button(
				__("Customer"),
				function () {
					artech_engine.model.open_mapped_doc({
						method: "artech.crm.doctype.prospect.prospect.make_customer",
						frm: frm,
					});
				},
				__("Create")
			);
		}
		if (!frm.is_new() && artech_engine.boot.user.can_create.includes("Opportunity")) {
			frm.add_custom_button(
				__("Opportunity"),
				function () {
					artech_engine.model.open_mapped_doc({
						method: "artech.crm.doctype.prospect.prospect.make_opportunity",
						frm: frm,
					});
				},
				__("Create")
			);
		}

		if (!frm.is_new()) {
			artech_engine.contacts.render_address_and_contact(frm);
		} else {
			artech_engine.contacts.clear_address_and_contact(frm);
		}
		frm.trigger("show_notes");
		frm.trigger("show_activities");
	},

	show_notes(frm) {
		const crm_notes = new artech.utils.CRMNotes({
			frm: frm,
			notes_wrapper: $(frm.fields_dict.notes_html.wrapper),
		});
		crm_notes.refresh();
	},

	show_activities(frm) {
		const crm_activities = new artech.utils.CRMActivities({
			frm: frm,
			open_activities_wrapper: $(frm.fields_dict.open_activities_html.wrapper),
			all_activities_wrapper: $(frm.fields_dict.all_activities_html.wrapper),
			form_wrapper: $(frm.wrapper),
		});
		crm_activities.refresh();
	},
});
