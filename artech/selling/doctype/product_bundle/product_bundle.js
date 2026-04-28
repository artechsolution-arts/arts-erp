// Copyright (c) 2021, Artech and Contributors
// License: GNU General Public License v3. See license.txt

artech_engine.ui.form.on("Product Bundle", {
	refresh: function (frm) {
		frm.toggle_enable("new_item_code", frm.is_new());
		frm.set_query("new_item_code", () => {
			return {
				query: "artech.selling.doctype.product_bundle.product_bundle.get_new_item_code",
			};
		});
	},
});
