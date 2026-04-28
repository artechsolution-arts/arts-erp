artech_engine.listview_settings["Stock Closing Entry"] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		return [__(doc.status), artech_engine.utils.guess_colour(doc.status), "status,=," + doc.status];
	},
};
