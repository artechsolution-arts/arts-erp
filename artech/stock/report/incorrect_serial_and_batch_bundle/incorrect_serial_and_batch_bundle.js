artech_engine.query_reports["Incorrect Serial and Batch Bundle"] = {
	filters: [
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
	],

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload(report) {
		report.page
			.add_inner_button(__("Fix SABB Entry"), () => {
				let indexes = artech_engine.query_report.datatable.rowmanager.getCheckedRows();
				let selected_rows = indexes.map((i) => artech_engine.query_report.data[i]);

				if (!selected_rows.length) {
					artech_engine.throw(__("Please select at least one row to fix"));
				} else {
					artech_engine.call({
						method: "artech.stock.report.incorrect_serial_and_batch_bundle.incorrect_serial_and_batch_bundle.fix_sabb_entries",
						freeze: true,
						args: {
							selected_rows: selected_rows,
						},
						callback: function (r) {
							artech_engine.query_report.refresh();
						},
					});
				}
			})
			.addClass("btn-primary");
	},
};
