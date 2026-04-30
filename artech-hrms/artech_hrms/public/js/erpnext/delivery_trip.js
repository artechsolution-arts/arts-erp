artech_engine.ui.form.on("Delivery Trip", {
	refresh: function (frm) {
		if (frm.doc.docstatus === 1 && frm.doc.employee) {
			frm.add_custom_button(
				__("Expense Claim"),
				function () {
					artech_engine.model.open_mapped_doc({
						method: "artech_hrms.hr.doctype.expense_claim.expense_claim.make_expense_claim_for_delivery_trip",
						frm: frm,
					});
				},
				__("Create"),
			);
		}
	},
});
