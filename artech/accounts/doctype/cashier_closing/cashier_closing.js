// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

artech_engine.ui.form.on("Cashier Closing", {
	setup: function (frm) {
		if (frm.doc.user == "" || frm.doc.user == null) {
			frm.doc.user = artech_engine.session.user;
		}
	},
});
