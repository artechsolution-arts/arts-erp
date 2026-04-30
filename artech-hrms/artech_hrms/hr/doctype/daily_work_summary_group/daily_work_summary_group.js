artech_engine.ui.form.on("Daily Work Summary Group", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Daily Work Summary"), function () {
				artech_engine.set_route("List", "Daily Work Summary");
			});
		}
	},
});
