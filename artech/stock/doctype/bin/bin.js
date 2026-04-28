artech_engine.ui.form.on("Bin", {
	refresh(frm) {
		frm.trigger("recalculate_bin_quantity");
	},

	recalculate_bin_quantity(frm) {
		frm.add_custom_button(__("Recalculate Bin Qty"), () => {
			artech_engine.call({
				method: "recalculate_qty",
				freeze: true,
				doc: frm.doc,
				callback: function (r) {
					artech_engine.show_alert(__("Bin Qty Recalculated"), 2);
				},
			});
		});
	},
});
