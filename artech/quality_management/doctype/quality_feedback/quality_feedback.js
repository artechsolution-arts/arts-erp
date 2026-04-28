// Copyright (c) 2019, Artech and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Quality Feedback", {
	template: function (frm) {
		if (frm.doc.template) {
			frm.call("set_parameters");
		}
	},
});
