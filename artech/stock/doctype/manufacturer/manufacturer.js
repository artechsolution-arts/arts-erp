// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Manufacturer", {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			hide_field(["address_html", "contact_html"]);
			artech_engine.contacts.clear_address_and_contact(frm);
		} else {
			unhide_field(["address_html", "contact_html"]);
			artech_engine.contacts.render_address_and_contact(frm);
		}
	},
});
