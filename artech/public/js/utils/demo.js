artech_engine.provide("artech.demo");

$(document).on("desktop_screen", function (event, data) {
	data.desktop.add_menu_item({
		label: __("Delete Demo Data"),
		icon: "trash",
		condition: function () {
			return artech_engine.boot.sysdefaults.demo_company;
		},
		onClick: function () {
			return artech.demo.clear_demo();
		},
	});
});

artech.demo.clear_demo = function () {
	artech_engine.confirm(__("Are you sure you want to clear all demo data?"), () => {
		artech_engine.call({
			method: "artech.setup.demo.clear_demo_data",
			freeze: true,
			freeze_message: __("Clearing Demo Data..."),
			callback: function (r) {
				artech_engine.ui.toolbar.clear_cache();
				artech_engine.show_alert({
					message: __("Demo data cleared"),
					indicator: "green",
				});
			},
		});
	});
};
