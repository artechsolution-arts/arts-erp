// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Advance Payment Ledger Entry", {
	refresh(frm) {
		frm.page.btn_secondary.hide();
		frm.set_currency_labels(["amount"], frm.doc.currency);
		frm.set_currency_labels(["base_amount"], artech.get_currency(frm.doc.company));
	},
});
