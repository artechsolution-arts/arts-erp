artech_engine.pages["visual-plant-floor"].on_page_load = function (wrapper) {
	var page = artech_engine.ui.make_app_page({
		parent: wrapper,
		title: "Visual Plant Floor",
		single_column: true,
	});

	artech_engine.visual_plant_floor = new artech_engine.ui.VisualPlantFloor(
		{ wrapper: $(wrapper).find(".layout-main-section") },
		wrapper.page
	);
};
