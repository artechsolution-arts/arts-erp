// Copyright (c) 2021, Artech and contributors
// For license information, please see license.txt

artech_engine.ui.form.on("Campaign", {
	refresh: function (frm) {
		artech.toggle_naming_series();

		if (frm.is_new()) {
			frm.toggle_display(
				"naming_series",
				artech_engine.boot.sysdefaults.campaign_naming_by == "Naming Series"
			);
		} else {
			frm.add_custom_button(
				__("View Leads"),
				function () {
					artech_engine.route_options = { utm_source: "Campaign", utm_campaign: frm.doc.name };
					artech_engine.set_route("List", "Lead");
				},
				"fa fa-list",
				true
			);
		}
	},
});
