artech_engine.ui.form.on("Advance Payment Ledger Entry", {
	refresh(frm) {
		frm.page.btn_secondary.hide();
		frm.set_currency_labels(["amount"], frm.doc.currency);
		frm.set_currency_labels(["base_amount"], artech.get_currency(frm.doc.company));
	},
});
