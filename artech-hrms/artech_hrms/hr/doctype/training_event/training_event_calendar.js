artech_engine.views.calendar["Training Event"] = {
	field_map: {
		start: "start_time",
		end: "end_time",
		id: "name",
		title: "event_name",
		allDay: "allDay",
	},
	gantt: true,
	get_events_method: "artech_engine.desk.calendar.get_events",
};
