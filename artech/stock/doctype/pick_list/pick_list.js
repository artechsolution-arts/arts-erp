artech_engine.ui.form.on("Pick List", {
	after_save(frm) {
		setTimeout(() => {
			// Added to fix the issue of locations table not getting updated after save
			frm.reload_doc();
		}, 500);
	},

	setup: (frm) => {
		frm.ignore_doctypes_on_cancel_all = ["Serial and Batch Bundle"];

		frm.set_indicator_formatter("item_code", function (doc) {
			return doc.stock_qty === 0 ? "red" : "green";
		});

		frm.custom_make_buttons = {
			"Delivery Note": "Delivery Note",
			"Stock Entry": "Stock Entry",
		};

		frm.set_query("warehouse", "locations", () => {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("parent_warehouse", () => {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("work_order", () => {
			return {
				query: "artech.stock.doctype.pick_list.pick_list.get_pending_work_orders",
				filters: {
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("material_request", () => {
			return {
				filters: {
					material_request_type: ["=", frm.doc.purpose],
				},
			};
		});

		frm.set_query("item_code", "locations", () => {
			return artech.queries.item({ is_stock_item: 1 });
		});

		frm.set_query("batch_no", "locations", (frm, cdt, cdn) => {
			const row = locals[cdt][cdn];
			return {
				query: "artech.controllers.queries.get_batch_no",
				filters: {
					item_code: row.item_code,
					warehouse: row.warehouse,
				},
			};
		});

		frm.set_query("serial_and_batch_bundle", "locations", (doc, cdt, cdn) => {
			let row = locals[cdt][cdn];
			return {
				filters: {
					item_code: row.item_code,
					voucher_type: doc.doctype,
					voucher_no: ["in", [doc.name, ""]],
					is_cancelled: 0,
				},
			};
		});
	},
	set_item_locations: (frm, save) => {
		if (!(frm.doc.locations && frm.doc.locations.length)) {
			artech_engine.msgprint(__("Add items in the Item Locations table"));
		} else {
			artech_engine.call({
				method: "set_item_locations",
				doc: frm.doc,
				args: {
					save: save,
				},
				freeze: 1,
				freeze_message: __("Setting Item Locations..."),
				callback(r) {
					refresh_field("locations");
				},
			});
		}
	},

	pick_manually: (frm) => {
		frm.trigger("update_warehouse_property");
	},

	update_warehouse_property: (frm) => {
		frm.fields_dict.locations.grid.update_docfield_property(
			"warehouse",
			"read_only",
			!frm.doc.pick_manually
		);
	},

	get_item_locations: (frm) => {
		// Button on the form
		frm.events.set_item_locations(frm, false);
	},
	refresh: (frm) => {
		frm.trigger("add_get_items_button");
		frm.trigger("update_warehouse_property");
		artech.toggle_serial_batch_fields(frm);

		if (frm.doc.docstatus === 1) {
			const status_completed = frm.doc.status === "Completed";

			if (!status_completed) {
				frm.add_custom_button(__("Update Current Stock"), () =>
					frm.trigger("update_pick_list_stock")
				);

				if (frm.doc.purpose === "Delivery") {
					frm.add_custom_button(
						__("Delivery Note"),
						() => frm.trigger("create_delivery_note"),
						__("Create")
					);
				} else {
					frm.add_custom_button(
						__("Stock Entry"),
						() => frm.trigger("create_stock_entry"),
						__("Create")
					);
				}
			}

			if (frm.doc.purpose === "Delivery" && frm.doc.status === "Open") {
				if (frm.doc.__onload && frm.doc.__onload.has_unreserved_stock) {
					frm.add_custom_button(
						__("Reserve"),
						() => frm.events.create_stock_reservation_entries(frm),
						__("Stock Reservation")
					);
				}

				if (frm.doc.__onload && frm.doc.__onload.has_reserved_stock) {
					frm.add_custom_button(
						__("Unreserve"),
						() => {
							artech_engine.confirm(
								__(
									"The reserved stock will be released. Are you certain you wish to proceed?"
								),
								() => frm.events.cancel_stock_reservation_entries(frm)
							);
						},
						__("Stock Reservation")
					);
					frm.add_custom_button(
						__("Reserved Stock"),
						() => frm.events.show_reserved_stock(frm),
						__("Stock Reservation")
					);
				}
			}
		}

		let sbb_field = frm.get_docfield("locations", "serial_and_batch_bundle");
		if (sbb_field) {
			sbb_field.get_route_options_for_new_doc = (row) => {
				return {
					item_code: row.doc.item_code,
					warehouse: row.doc.warehouse,
					voucher_type: frm.doc.doctype,
				};
			};
		}
	},
	work_order: (frm) => {
		artech_engine.db
			.get_value("Work Order", frm.doc.work_order, ["qty", "material_transferred_for_manufacturing"])
			.then((data) => {
				let qty_data = data.message;
				let max = qty_data.qty - qty_data.material_transferred_for_manufacturing;
				artech_engine.prompt(
					{
						fieldtype: "Float",
						label: __("Qty of Finished Goods Item"),
						fieldname: "qty",
						description: __("Max: {0}", [max]),
						default: max,
					},
					(data) => {
						frm.set_value("for_qty", data.qty);
						if (data.qty > max) {
							artech_engine.msgprint(__("Quantity must not be more than {0}", [max]));
							return;
						}
						frm.clear_table("locations");
						artech.utils.map_current_doc({
							method: "artech.manufacturing.doctype.work_order.work_order.create_pick_list",
							target: frm,
							source_name: frm.doc.work_order,
						});
					},
					__("Select Quantity"),
					__("Get Items")
				);
			});
	},
	material_request: (frm) => {
		artech.utils.map_current_doc({
			method: "artech.stock.doctype.material_request.material_request.create_pick_list",
			target: frm,
			source_name: frm.doc.material_request,
		});
	},
	purpose: (frm) => {
		frm.clear_table("locations");
		frm.trigger("add_get_items_button");
	},
	create_delivery_note: (frm) => {
		artech_engine.model.open_mapped_doc({
			method: "artech.stock.doctype.pick_list.pick_list.create_delivery_note",
			frm: frm,
		});
	},
	create_stock_entry: (frm) => {
		artech_engine
			.xcall("artech.stock.doctype.pick_list.pick_list.create_stock_entry", {
				pick_list: frm.doc,
			})
			.then((stock_entry) => {
				artech_engine.model.sync(stock_entry);
				artech_engine.set_route("Form", "Stock Entry", stock_entry.name);
			});
	},
	update_pick_list_stock: (frm) => {
		frm.events.set_item_locations(frm, true);
	},
	add_get_items_button: (frm) => {
		let purpose = frm.doc.purpose;
		if (purpose != "Delivery" || frm.doc.docstatus !== 0) return;
		let get_query_filters = {
			docstatus: 1,
			per_delivered: ["<", 100],
			status: ["!=", ""],
			customer: frm.doc.customer,
		};
		frm.get_items_btn = frm.add_custom_button(__("Get Items"), () => {
			artech.utils.map_current_doc({
				method: "artech.selling.doctype.sales_order.sales_order.create_pick_list",
				source_doctype: "Sales Order",
				target: frm,
				setters: {
					company: frm.doc.company,
					customer: frm.doc.customer,
				},
				date_field: "transaction_date",
				get_query_filters: get_query_filters,
			});
		});
	},
	scan_barcode: (frm) => {
		const opts = {
			frm,
			items_table_name: "locations",
			qty_field: "picked_qty",
			max_qty_field: "qty",
			dont_allow_new_row: true,
			prompt_qty: frm.doc.prompt_qty,
			serial_no_field: "not_supported", // doesn't make sense for picklist without a separate field.
		};
		const barcode_scanner = new artech.utils.BarcodeScanner(opts);
		barcode_scanner.process_scan();
	},
	create_stock_reservation_entries: (frm) => {
		artech_engine.call({
			doc: frm.doc,
			method: "create_stock_reservation_entries",
			args: {
				notify: true,
			},
			freeze: true,
			freeze_message: __("Reserving Stock..."),
			callback: (r) => {
				frm.doc.__onload.has_unreserved_stock = false;
				frm.reload_doc();
			},
		});
	},
	cancel_stock_reservation_entries: (frm) => {
		artech_engine.call({
			doc: frm.doc,
			method: "cancel_stock_reservation_entries",
			args: {
				notify: true,
			},
			freeze: true,
			freeze_message: __("Unreserving Stock..."),
			callback: (r) => {
				frm.doc.__onload.has_reserved_stock = false;
				frm.reload_doc();
			},
		});
	},
	show_reserved_stock(frm) {
		// Get the latest modified date from the locations table.
		var to_date = moment(
			new Date(Math.max(...frm.doc.locations.map((e) => new Date(e.modified))))
		).format("YYYY-MM-DD");

		artech_engine.route_options = {
			company: frm.doc.company,
			from_date: moment(frm.doc.creation).format("YYYY-MM-DD"),
			to_date: to_date,
			voucher_type: "Sales Order",
			from_voucher_type: "Pick List",
			from_voucher_no: frm.doc.name,
		};
		artech_engine.set_route("query-report", "Reserved Stock");
	},
});

artech_engine.ui.form.on("Pick List Item", {
	item_code: (frm, cdt, cdn) => {
		let row = artech_engine.get_doc(cdt, cdn);
		if (row.item_code) {
			get_item_details(row.item_code, row.uom, row.warehouse, frm.doc.company).then((data) => {
				artech_engine.model.set_value(cdt, cdn, "uom", data.stock_uom);
				artech_engine.model.set_value(cdt, cdn, "stock_uom", data.stock_uom);
				artech_engine.model.set_value(cdt, cdn, "conversion_factor", 1);
				artech_engine.model.set_value(cdt, cdn, "actual_qty", data.actual_qty);
				artech_engine.model.set_value(cdt, cdn, "company_total_stock", data.company_total_stock);
			});
		}
	},

	uom: (frm, cdt, cdn) => {
		let row = artech_engine.get_doc(cdt, cdn);
		if (row.uom) {
			get_item_details(row.item_code, row.uom).then((data) => {
				artech_engine.model.set_value(cdt, cdn, "conversion_factor", data.conversion_factor);
			});
		}
	},

	warehouse: (frm, cdt, cdn) => {
		const row = artech_engine.get_doc(cdt, cdn);
		if (!row.item_code || !row.warehouse) return;
		get_item_details(row.item_code, row.uom, row.warehouse, frm.doc.company).then((data) => {
			artech_engine.model.set_value(cdt, cdn, "actual_qty", data.actual_qty);
			artech_engine.model.set_value(cdt, cdn, "company_total_stock", data.company_total_stock);
		});
	},

	qty: (frm, cdt, cdn) => {
		let row = artech_engine.get_doc(cdt, cdn);
		artech_engine.model.set_value(cdt, cdn, "stock_qty", row.qty * row.conversion_factor);
	},

	conversion_factor: (frm, cdt, cdn) => {
		let row = artech_engine.get_doc(cdt, cdn);
		artech_engine.model.set_value(cdt, cdn, "stock_qty", row.qty * row.conversion_factor);
	},

	pick_serial_and_batch(frm, cdt, cdn) {
		let item = locals[cdt][cdn];
		let path = "assets/artech/js/utils/serial_no_batch_selector.js";

		artech_engine.db.get_value("Item", item.item_code, ["has_batch_no", "has_serial_no"]).then((r) => {
			if (r.message && (r.message.has_batch_no || r.message.has_serial_no)) {
				item.has_serial_no = r.message.has_serial_no;
				item.has_batch_no = r.message.has_batch_no;
				item.type_of_transaction = item.qty > 0 ? "Outward" : "Inward";

				item.title = item.has_serial_no ? __("Select Serial No") : __("Select Batch No");

				if (item.has_serial_no && item.has_batch_no) {
					item.title = __("Select Serial and Batch");
				}

				new artech.SerialBatchPackageSelector(frm, item, (r) => {
					if (r) {
						let qty = Math.abs(r.total_qty);
						artech_engine.model.set_value(item.doctype, item.name, {
							serial_and_batch_bundle: r.name,
							use_serial_batch_fields: 0,
							qty: qty / flt(item.conversion_factor || 1, precision("conversion_factor", item)),
						});
					}
				});
			}
		});
	},
});

function get_item_details(item_code, uom = null, warehouse = null, company = null) {
	if (item_code) {
		return artech_engine.xcall("artech.stock.doctype.pick_list.pick_list.get_item_details", {
			item_code,
			uom,
			warehouse,
			company,
		});
	}
}
