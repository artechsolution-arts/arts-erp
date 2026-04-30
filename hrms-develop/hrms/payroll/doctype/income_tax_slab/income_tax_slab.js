artech_engine.ui.form.on("Income Tax Slab", {
	refresh: function (frm) {
		if (frm.doc.docstatus != 1) return;
		frm.add_custom_button(
			__("Salary Structure Assignment"),
			() => {
				artech_engine.model.with_doctype("Salary Structure Assignment", () => {
					const doc = artech_engine.model.get_new_doc("Salary Structure Assignment");
					doc.income_tax_slab = frm.doc.name;
					artech_engine.set_route("Form", "Salary Structure Assignment", doc.name);
				});
			},
			__("Create"),
		);
		frm.page.set_inner_btn_group_as_primary(__("Create"));
	},

	currency: function (frm) {
		frm.refresh_fields();
	},
});
