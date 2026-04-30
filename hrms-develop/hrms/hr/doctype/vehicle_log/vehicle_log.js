artech_engine.ui.form.on("Vehicle Log", {
	setup: function (frm) {
		frm.set_query("employee", function () {
			return {
				filters: {
					status: "Active",
				},
			};
		});
	},
	refresh: function (frm) {
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button(
				__("Expense Claim"),
				function () {
					frm.events.expense_claim(frm);
				},
				__("Create"),
			);
			frm.page.set_inner_btn_group_as_primary(__("Create"));
		}
	},

	expense_claim: function (frm) {
		artech_engine.call({
			method: "hrms.hr.doctype.vehicle_log.vehicle_log.make_expense_claim",
			args: {
				docname: frm.doc.name,
			},
			callback: function (r) {
				var doc = artech_engine.model.sync(r.message);
				artech_engine.set_route("Form", "Expense Claim", r.message.name);
			},
		});
	},
});
