artech_engine.ui.form.on("Employee Benefit Ledger", {
	refresh: (frm) => {
		frm.set_read_only();
		frm.page.btn_primary.hide();
	},
});
