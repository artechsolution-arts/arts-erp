// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Delivery Trip", {
	setup: function (frm) {
		frm.set_indicator_formatter("customer", (stop) => (stop.visited ? "green" : "orange"));

		frm.set_query("driver", function () {
			return {
				filters: {
					status: "Active",
				},
			};
		});

		frm.set_query("address", "delivery_stops", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (row.customer) {
				return {
					query: "artech_engine.contacts.doctype.address.address.address_query",
					filters: {
						link_doctype: "Customer",
						link_name: row.customer,
					},
				};
			}
		});

		frm.set_query("contact", "delivery_stops", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (row.customer) {
				return {
					query: "artech_engine.contacts.doctype.contact.contact.contact_query",
					filters: {
						link_doctype: "Customer",
						link_name: row.customer,
					},
				};
			}
		});
	},

	refresh: function (frm) {
		frm.ignore_doctypes_on_cancel_all = ["Delivery Note"];

		if (frm.doc.docstatus == 1 && frm.doc.delivery_stops.length > 0) {
			frm.add_custom_button(__("Notify Customers via Email"), function () {
				frm.trigger("notify_customers");
			});
		}

		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(
				__("Delivery Note"),
				() => {
					artech.utils.map_current_doc({
						method: "artech.stock.doctype.delivery_note.delivery_note.make_delivery_trip",
						source_doctype: "Delivery Note",
						target: frm,
						date_field: "posting_date",
						setters: {
							company: frm.doc.company,
							customer: null,
						},
						get_query_filters: {
							company: frm.doc.company,
							status: ["Not In", ["Completed", "Cancelled"]],
						},
					});
				},
				__("Get stops from")
			);
		}
		frm.add_custom_button(
			__("Delivery Notes"),
			function () {
				artech_engine.set_route("List", "Delivery Note", {
					name: [
						"in",
						frm.doc.delivery_stops.map((stop) => {
							return stop.delivery_note;
						}),
					],
				});
			},
			__("View")
		);
	},

	calculate_arrival_time: function (frm) {
		if (!frm.doc.driver_address) {
			artech_engine.throw(__("Cannot Calculate Arrival Time as Driver Address is Missing."));
		}
		artech_engine.show_alert({
			message: "Calculating Arrival Times",
			indicator: "orange",
		});
		frm.call(
			"process_route",
			{
				optimize: false,
			},
			() => {
				frm.reload_doc();
			}
		);
	},

	driver: function (frm) {
		if (frm.doc.driver) {
			artech_engine.call({
				method: "artech.stock.doctype.delivery_trip.delivery_trip.get_driver_email",
				args: {
					driver: frm.doc.driver,
				},
				callback: (data) => {
					frm.set_value("driver_email", data.message.email);
				},
			});
		}
	},

	optimize_route: function (frm) {
		if (!frm.doc.driver_address) {
			artech_engine.throw(__("Cannot Optimize Route as Driver Address is Missing."));
		}
		artech_engine.show_alert({
			message: "Optimizing Route",
			indicator: "orange",
		});
		frm.call(
			"process_route",
			{
				optimize: true,
			},
			() => {
				frm.reload_doc();
			}
		);
	},

	notify_customers: function (frm) {
		$.each(frm.doc.delivery_stops || [], function (i, delivery_stop) {
			if (!delivery_stop.delivery_note) {
				artech_engine.msgprint({
					message: __("No Delivery Note selected for Customer {}", [delivery_stop.customer]),
					title: __("Warning"),
					indicator: "orange",
					alert: 1,
				});
			}
		});

		artech_engine.db.get_value("Delivery Settings", { name: "Delivery Settings" }, "dispatch_template", (r) => {
			if (!r.dispatch_template) {
				artech_engine.throw(__("Missing email template for dispatch. Please set one in Delivery Settings."));
			} else {
				artech_engine.confirm(__("Do you want to notify all the customers by email?"), function () {
					artech_engine.call({
						method: "artech.stock.doctype.delivery_trip.delivery_trip.notify_customers",
						args: {
							delivery_trip: frm.doc.name,
						},
						callback: function (r) {
							if (!r.exc) {
								frm.doc.email_notification_sent = true;
								frm.refresh_field("email_notification_sent");
							}
						},
					});
				});
			}
		});
	},
});

artech_engine.ui.form.on("Delivery Stop", {
	customer: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.customer) {
			artech_engine.call({
				method: "artech.stock.doctype.delivery_trip.delivery_trip.get_contact_and_address",
				args: { name: row.customer },
				callback: function (r) {
					if (r.message) {
						if (r.message["shipping_address"]) {
							artech_engine.model.set_value(cdt, cdn, "address", r.message["shipping_address"].parent);
						} else {
							artech_engine.model.set_value(cdt, cdn, "address", "");
						}
						if (r.message["contact_person"]) {
							artech_engine.model.set_value(cdt, cdn, "contact", r.message["contact_person"].parent);
						} else {
							artech_engine.model.set_value(cdt, cdn, "contact", "");
						}
					} else {
						artech_engine.model.set_value(cdt, cdn, "address", "");
						artech_engine.model.set_value(cdt, cdn, "contact", "");
					}
				},
			});
		}
	},

	address: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.address) {
			artech_engine.call({
				method: "artech_engine.contacts.doctype.address.address.get_address_display",
				args: { address_dict: row.address },
				callback: function (r) {
					if (r.message) {
						artech_engine.model.set_value(
							cdt,
							cdn,
							"customer_address",
							artech_engine.utils.html2text(r.message)
						);
					}
				},
			});
		} else {
			artech_engine.model.set_value(cdt, cdn, "customer_address", "");
		}
	},

	contact: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.contact) {
			artech_engine.call({
				method: "artech.stock.doctype.delivery_trip.delivery_trip.get_contact_display",
				args: { contact: row.contact },
				callback: function (r) {
					if (r.message) {
						artech_engine.model.set_value(cdt, cdn, "customer_contact", r.message);
					}
				},
			});
		} else {
			artech_engine.model.set_value(cdt, cdn, "customer_contact", "");
		}
	},
});
