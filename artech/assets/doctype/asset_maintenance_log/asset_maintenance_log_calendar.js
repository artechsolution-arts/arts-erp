artech_engine.views.calendar["Asset Maintenance Log"] = {
	field_map: {
		start: "due_date",
		end: "due_date",
		id: "name",
		title: "task",
		allDay: "allDay",
		progress: "progress",
	},
	filters: [
		{
			fieldtype: "Link",
			fieldname: "asset_name",
			options: "Asset Maintenance",
			label: __("Asset Maintenance"),
		},
	],
	get_events_method: "artech_engine.desk.calendar.get_events",
};
