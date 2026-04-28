// Copyright (c) 2015, Artech and Contributors

artech_engine.views.calendar["Holiday List"] = {
	field_map: {
		start: "holiday_date",
		end: "holiday_date",
		id: "name",
		title: "description",
		allDay: "allDay",
	},
	order_by: `from_date`,
	get_events_method: "artech.setup.doctype.holiday_list.holiday_list.get_events",
	filters: [
		{
			fieldtype: "Link",
			fieldname: "holiday_list",
			options: "Holiday List",
			label: __("Holiday List"),
		},
	],
};
