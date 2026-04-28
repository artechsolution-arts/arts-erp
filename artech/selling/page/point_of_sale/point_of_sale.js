artech_engine.provide("artech.PointOfSale");

artech_engine.pages["point-of-sale"].on_page_load = function (wrapper) {
	artech_engine.ui.make_app_page({
		parent: wrapper,
		title: __("Point of Sale"),
		single_column: true,
		hide_sidebar: true,
	});

	artech_engine.require("point-of-sale.bundle.js", function () {
		wrapper.pos = new artech.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	});
};

artech_engine.pages["point-of-sale"].refresh = function (wrapper) {
	if (document.scannerDetectionData) {
		onScan.detachFrom(document);
		wrapper.pos.wrapper.html("");
		wrapper.pos.check_opening_entry();
	}
};
