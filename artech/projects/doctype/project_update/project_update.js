// Copyright (c) 2018, Artech and contributors

artech_engine.ui.form.on("Project Update", {
	refresh: function () {},

	onload: function (frm) {
		frm.set_value("naming_series", "UPDATE-.project.-.YY.MM.DD.-.####");
	},

	validate: function (frm) {
		frm.set_value("time", artech_engine.datetime.now_time());
		frm.set_value("date", artech_engine.datetime.nowdate());
	},
});
