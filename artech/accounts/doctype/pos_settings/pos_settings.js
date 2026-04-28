let search_fields_datatypes = [
	"Data",
	"Link",
	"Dynamic Link",
	"Long Text",
	"Select",
	"Small Text",
	"Text",
	"Text Editor",
];
let do_not_include_fields = [
	"naming_series",
	"item_code",
	"item_name",
	"stock_uom",
	"asset_naming_series",
	"default_material_request_type",
	"valuation_method",
	"warranty_period",
	"weight_uom",
	"batch_number_series",
	"serial_no_series",
	"purchase_uom",
	"customs_tariff_number",
	"sales_uom",
	"deferred_revenue_account",
	"deferred_expense_account",
	"quality_inspection_template",
	"route",
	"slideshow",
	"website_image_alt",
	"thumbnail",
	"web_long_description",
];

artech_engine.ui.form.on("POS Settings", {
	onload: function (frm) {
		frm.trigger("get_invoice_fields");
		frm.trigger("add_search_options");
	},

	get_invoice_fields: function (frm) {
		artech_engine.model.with_doctype("POS Invoice", () => {
			var fields = $.map(artech_engine.get_doc("DocType", "POS Invoice").fields, function (d) {
				if (
					artech_engine.model.no_value_type.indexOf(d.fieldtype) === -1 ||
					["Button"].includes(d.fieldtype)
				) {
					return { label: d.label + " (" + d.fieldtype + ")", value: d.fieldname };
				} else {
					return null;
				}
			});

			frm.fields_dict.invoice_fields.grid.update_docfield_property(
				"fieldname",
				"options",
				[""].concat(fields)
			);
		});
	},

	add_search_options: function (frm) {
		artech_engine.model.with_doctype("Item", () => {
			var fields = $.map(artech_engine.get_doc("DocType", "Item").fields, function (d) {
				if (
					search_fields_datatypes.includes(d.fieldtype) &&
					!do_not_include_fields.includes(d.fieldname)
				) {
					return [d.label];
				} else {
					return null;
				}
			});

			fields.unshift("");
			frm.fields_dict.pos_search_fields.grid.update_docfield_property("field", "options", fields);
		});
	},
});

artech_engine.ui.form.on("POS Search Fields", {
	field: function (frm, doctype, name) {
		var doc = artech_engine.get_doc(doctype, name);
		var df = $.map(artech_engine.get_doc("DocType", "Item").fields, function (d) {
			if (doc.field == d.label && search_fields_datatypes.includes(d.fieldtype)) {
				return d;
			} else {
				return null;
			}
		})[0];

		doc.fieldname = df.fieldname;
		frm.refresh_field("fields");
	},
});

artech_engine.ui.form.on("POS Field", {
	fieldname: function (frm, doctype, name) {
		var doc = artech_engine.get_doc(doctype, name);
		var df = $.map(artech_engine.get_doc("DocType", "POS Invoice").fields, function (d) {
			return doc.fieldname == d.fieldname ? d : null;
		})[0];

		doc.label = df.label;
		doc.reqd = df.reqd;
		doc.options = df.options;
		doc.fieldtype = df.fieldtype;
		doc.default_value = df.default;
		frm.refresh_field("fields");
	},
});
