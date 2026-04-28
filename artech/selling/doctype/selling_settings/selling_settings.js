// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Selling Settings", {
	after_save(frm) {
		artech_engine.boot.user.defaults.editable_price_list_rate = frm.doc.editable_price_list_rate;
	},
});
