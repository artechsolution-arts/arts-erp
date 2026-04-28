artech_engine.ui.form.on("Item Tax Template", {
	setup: function (frm) {
		frm.set_query("tax_type", "taxes", function (doc) {
			return {
				filters: [
					["Account", "company", "=", frm.doc.company],
					["Account", "is_group", "=", 0],
					[
						"Account",
						"account_type",
						"in",
						[
							"Tax",
							"Chargeable",
							"Income Account",
							"Expense Account",
							"Expenses Included In Valuation",
						],
					],
				],
			};
		});
	},
	company: function (frm) {
		frm.set_query("tax_type", "taxes", function (doc) {
			return {
				filters: [
					["Account", "company", "=", frm.doc.company],
					["Account", "is_group", "=", 0],
					[
						"Account",
						"account_type",
						"in",
						[
							"Tax",
							"Chargeable",
							"Income Account",
							"Expense Account",
							"Expenses Included In Valuation",
						],
					],
				],
			};
		});
	},
});

artech_engine.ui.form.on("Item Tax Template Detail", {
	not_applicable: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.not_applicable) {
			artech_engine.model.set_value(cdt, cdn, "tax_rate", 0);
		}
	},
});
