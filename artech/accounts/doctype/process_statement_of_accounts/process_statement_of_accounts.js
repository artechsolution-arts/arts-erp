artech_engine.ui.form.on("Process Statement Of Accounts", {
	view_properties: function (frm) {
		artech_engine.route_options = { doc_type: "Customer" };
		artech_engine.set_route("Form", "Customize Form");
	},
	refresh: function (frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Send Emails"), function () {
				if (frm.is_dirty()) artech_engine.throw(__("Please save before proceeding."));
				artech_engine.call({
					method: "artech.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.send_emails",
					args: {
						document_name: frm.doc.name,
					},
					callback: function (r) {
						if (r && r.message) {
							artech_engine.show_alert({ message: __("Emails Queued"), indicator: "blue" });
						} else {
							artech_engine.msgprint(__("No Records for these settings."));
						}
					},
				});
			});
			frm.add_custom_button(__("Download"), function () {
				if (frm.is_dirty()) artech_engine.throw(__("Please save before proceeding."));
				let url = artech_engine.urllib.get_full_url(
					"/api/method/artech.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.download_statements?" +
						"document_name=" +
						encodeURIComponent(frm.doc.name)
				);
				$.ajax({
					url: url,
					type: "GET",
					success: function (result) {
						if (jQuery.isEmptyObject(result)) {
							artech_engine.msgprint(__("No Records for these settings."));
						} else {
							window.location = url;
						}
					},
				});
			});
		}
	},
	onload: function (frm) {
		frm.set_query("currency", function () {
			return {
				filters: {
					enabled: 1,
				},
			};
		});
		frm.set_query("account", function () {
			if (!frm.doc.company) {
				artech_engine.throw(__("Please set Company"));
			}
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
		frm.set_query("cost_center", function () {
			if (!frm.doc.company) {
				artech_engine.throw(__("Please set Company"));
			}
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
		frm.set_query("project", function () {
			if (!frm.doc.company) {
				artech_engine.throw(__("Please set Company"));
			}
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
		frm.set_query("print_format", function () {
			return {
				filters: {
					print_format_for: "Report",
					report: frm.doc.report,
					disabled: 0,
					print_format_type: "Jinja",
				},
			};
		});
		if (frm.doc.__islocal) {
			frm.set_value("from_date", artech_engine.datetime.add_months(artech_engine.datetime.get_today(), -1));
			frm.set_value("to_date", artech_engine.datetime.get_today());
		}
	},
	company: function (frm) {
		frm.set_value("account", "");
		frm.set_value("cost_center", "");
		frm.set_value("project", "");
		artech.utils.set_letter_head(frm);
	},
	report: function (frm) {
		let filters = {
			company: frm.doc.company,
		};
		if (frm.doc.report == "Accounts Receivable") {
			filters["account_type"] = "Receivable";
		}
		frm.set_query("account", function () {
			return {
				filters: filters,
			};
		});
		frm.set_query("print_format", function () {
			return {
				filters: {
					print_format_for: "Report",
					report: frm.doc.report,
					disabled: 0,
					print_format_type: "Jinja",
				},
			};
		});
	},
	customer_collection: function (frm) {
		frm.set_value("collection_name", "");
		if (frm.doc.customer_collection) {
			frm.get_field("collection_name").set_label(frm.doc.customer_collection);
		}
	},
	frequency: function (frm) {
		if (frm.doc.frequency != "") {
			frm.set_value("start_date", artech_engine.datetime.get_today());
		} else {
			frm.set_value("start_date", "");
		}
	},
	fetch_customers: function (frm) {
		if (frm.doc.collection_name) {
			artech_engine.call({
				method: "artech.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.fetch_customers",
				args: {
					customer_collection: frm.doc.customer_collection,
					collection_name: frm.doc.collection_name,
					primary_mandatory: frm.doc.primary_mandatory,
				},
				callback: function (r) {
					if (!r.exc) {
						if (r.message.length) {
							frm.clear_table("customers");
							for (const customer of r.message) {
								var row = frm.add_child("customers");
								row.customer = customer.name;
								row.primary_email = customer.primary_email;
								row.billing_email = customer.billing_email;
							}
							frm.refresh_field("customers");
						} else {
							artech_engine.throw(__("No Customers found with selected options."));
						}
					}
				},
			});
		} else {
			artech_engine.throw("Enter " + frm.doc.customer_collection + " name.");
		}
	},
});

artech_engine.ui.form.on("Process Statement Of Accounts Customer", {
	customer: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (!row.customer) {
			return;
		}
		artech_engine.call({
			method: "artech.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.get_customer_emails",
			args: {
				customer_name: row.customer,
				primary_mandatory: frm.doc.primary_mandatory,
			},
			callback: function (r) {
				if (!r.exe) {
					if (r.message.length) {
						artech_engine.model.set_value(cdt, cdn, "primary_email", r.message[0]);
						artech_engine.model.set_value(cdt, cdn, "billing_email", r.message[1]);
					} else {
						return;
					}
				}
			},
		});
	},
});
