// Copyright (c) 2015, Artech and Contributors
// License: GNU General Public License v3. See license.txt

artech_engine.provide("artech.stock");

artech.stock.StockController = class StockController extends artech_engine.ui.form.Controller {
	onload() {
		// warehouse query if company
		if (this.frm.fields_dict.company) {
			this.setup_warehouse_query();
		}
	}

	barcode(doc, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.barcode) {
			artech.stock.utils.set_item_details_using_barcode(this.frm, row, (r) => {
				artech_engine.model.set_value(cdt, cdn, {
					item_code: r.message.item_code,
					qty: 1,
				});
			});
		}
	}

	setup_warehouse_query() {
		var me = this;
		artech.queries.setup_queries(this.frm, "Warehouse", function () {
			return artech.queries.warehouse(me.frm.doc);
		});
	}

	setup_posting_date_time_check() {
		// make posting date default and read only unless explictly checked
		artech_engine.ui.form.on(this.frm.doctype, "set_posting_date_and_time_read_only", function (frm) {
			if (frm.doc.docstatus == 0 && frm.doc.set_posting_time) {
				frm.set_df_property("posting_date", "read_only", 0);
				frm.set_df_property("posting_time", "read_only", 0);
			} else {
				frm.set_df_property("posting_date", "read_only", 1);
				frm.set_df_property("posting_time", "read_only", 1);
			}
		});

		artech_engine.ui.form.on(this.frm.doctype, "set_posting_time", function (frm) {
			frm.trigger("set_posting_date_and_time_read_only");
		});

		artech_engine.ui.form.on(this.frm.doctype, "refresh", function (frm) {
			// set default posting date / time
			if (frm.doc.docstatus == 0) {
				if (!frm.doc.posting_date) {
					frm.set_value("posting_date", artech_engine.datetime.nowdate());
				}
				if (!frm.doc.posting_time) {
					frm.set_value("posting_time", artech_engine.datetime.now_time());
				}
				frm.trigger("set_posting_date_and_time_read_only");
			}
		});
	}

	show_stock_ledger() {
		var me = this;
		if (this.frm.doc.docstatus > 0) {
			cur_frm.add_custom_button(
				__("Stock Ledger"),
				function () {
					artech_engine.route_options = {
						voucher_no: me.frm.doc.name,
						from_date: me.frm.doc.posting_date,
						to_date: moment(me.frm.doc.modified).format("YYYY-MM-DD"),
						company: me.frm.doc.company,
						show_cancelled_entries: me.frm.doc.docstatus === 2,
						ignore_prepared_report: true,
					};
					artech_engine.set_route("query-report", "Stock Ledger");
				},
				__("View")
			);
		}
	}

	show_general_ledger() {
		let me = this;
		if (this.frm.doc.docstatus > 0) {
			cur_frm.add_custom_button(
				__("Accounting Ledger"),
				function () {
					artech_engine.route_options = {
						voucher_no: me.frm.doc.name,
						from_date: me.frm.doc.posting_date,
						to_date: moment(me.frm.doc.modified).format("YYYY-MM-DD"),
						company: me.frm.doc.company,
						categorize_by: "Categorize by Voucher (Consolidated)",
						show_cancelled_entries: me.frm.doc.docstatus === 2,
						ignore_prepared_report: true,
					};
					artech_engine.set_route("query-report", "General Ledger");
				},
				__("View")
			);
		}
	}
};
