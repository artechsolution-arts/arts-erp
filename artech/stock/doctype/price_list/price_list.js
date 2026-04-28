artech_engine.ui.form.on("Price List", {
	refresh: function (frm) {
		let me = this;
		frm.add_custom_button(
			__("Add / Edit Prices"),
			function () {
				artech_engine.route_options = {
					price_list: frm.doc.name,
				};
				artech_engine.set_route("Report", "Item Price");
			},
			"fa fa-money"
		);
	},
});
