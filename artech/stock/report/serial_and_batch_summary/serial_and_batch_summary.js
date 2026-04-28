/* eslint-disable */

artech_engine.query_reports["Serial and Batch Summary"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: artech_engine.defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: artech_engine.datetime.get_today(),
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			fieldname: "voucher_type",
			label: __("Voucher Type"),
			fieldtype: "Link",
			options: "DocType",
			get_query: function () {
				return {
					query: "artech.stock.report.serial_and_batch_summary.serial_and_batch_summary.get_voucher_type",
				};
			},
		},
		{
			fieldname: "voucher_no",
			label: __("Voucher No"),
			fieldtype: "MultiSelectList",
			options: "voucher_type",
			get_data: function (txt) {
				if (!artech_engine.query_report.filters) return;

				let voucher_type = artech_engine.query_report.get_filter_value("voucher_type");
				if (!voucher_type) return;

				return artech_engine.db.get_link_options(voucher_type, txt);
			},
		},
		{
			fieldname: "serial_no",
			label: __("Serial No"),
			fieldtype: "Link",
			options: "Serial No",
			get_query: function () {
				return {
					query: "artech.stock.report.serial_and_batch_summary.serial_and_batch_summary.get_serial_nos",
					filters: {
						item_code: artech_engine.query_report.get_filter_value("item_code"),
						voucher_type: artech_engine.query_report.get_filter_value("voucher_type"),
						voucher_no: artech_engine.query_report.get_filter_value("voucher_no"),
					},
				};
			},
		},
		{
			fieldname: "batch_no",
			label: __("Batch No"),
			fieldtype: "Link",
			options: "Batch",
			get_query: function () {
				return {
					query: "artech.stock.report.serial_and_batch_summary.serial_and_batch_summary.get_batch_nos",
					filters: {
						item_code: artech_engine.query_report.get_filter_value("item_code"),
						voucher_type: artech_engine.query_report.get_filter_value("voucher_type"),
						voucher_no: artech_engine.query_report.get_filter_value("voucher_no"),
					},
				};
			},
		},
	],
};
