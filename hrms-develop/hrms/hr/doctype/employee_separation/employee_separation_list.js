artech_engine.listview_settings["Employee Separation"] = {
	add_fields: ["boarding_status", "employee_name", "department"],
	filters: [["boarding_status", "=", "Pending"]],
	get_indicator: function (doc) {
		return [
			__(doc.boarding_status),
			artech_engine.utils.guess_colour(doc.boarding_status),
			"boarding_status,=," + doc.boarding_status,
		];
	},
};
