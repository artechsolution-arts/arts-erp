// Copyright (c) 2016, Artech and contributors

artech_engine.query_reports["Customer-wise Item Price"] = {
	filters: [
		{
			label: __("Customer"),
			fieldname: "customer",
			fieldtype: "Link",
			options: "Customer",
			reqd: 1,
		},
		{
			label: __("Item"),
			fieldname: "item",
			fieldtype: "Link",
			options: "Item",
			get_query: () => {
				return {
					query: "artech.controllers.queries.item_query",
					filters: { is_sales_item: 1 },
				};
			},
		},
	],
};
