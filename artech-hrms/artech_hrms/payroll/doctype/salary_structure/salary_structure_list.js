artech_engine.listview_settings["Salary Structure"] = {
	onload: function (list_view) {
		list_view.page.add_inner_button(__("Bulk Salary Structure Assignment"), function () {
			artech_engine.set_route("Form", "Bulk Salary Structure Assignment");
		});
	},
};
