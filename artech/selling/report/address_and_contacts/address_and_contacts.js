// Copyright (c) 2016, Artech and contributors
// For license information, please see license.txt

artech_engine.query_reports["Address And Contacts"] = {
	filters: [
		{
			reqd: 1,
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "DocType",
			get_query: function () {
				return {
					filters: {
						name: ["in", "Customer,Supplier,Sales Partner,Lead"],
					},
				};
			},
		},
		{
			fieldname: "party_name",
			label: __("Party Name"),
			fieldtype: "Dynamic Link",
			get_options: function () {
				let party_type = artech_engine.query_report.get_filter_value("party_type");
				if (!party_type) {
					artech_engine.throw(__("Please select Party Type first"));
				}
				return party_type;
			},
		},
	],
};
