import artech_engine


def execute():
	def cancel_incorrect_gl_entries(gl_entries):
		table = artech_engine.qb.DocType("GL Entry")
		artech_engine.qb.update(table).set(table.is_cancelled, 1).where(table.name.isin(gl_entries)).run()

	def recreate_gl_entries(voucher_nos):
		for doc in voucher_nos:
			doc = artech_engine.get_doc("Subcontracting Receipt", doc)
			for item in doc.supplied_items:
				account, cost_center = artech_engine.db.get_values(
					"Subcontracting Receipt Item", item.reference_name, ["expense_account", "cost_center"]
				)[0]

				if not item.expense_account:
					item.db_set("expense_account", account)
				if not item.cost_center:
					item.db_set("cost_center", cost_center)

			doc.make_gl_entries()

	docs = artech_engine.get_all(
		"GL Entry",
		fields=["name", "voucher_no"],
		filters={"voucher_type": "Subcontracting Receipt", "account": ["is", "not set"], "is_cancelled": 0},
	)

	if docs:
		cancel_incorrect_gl_entries([d.name for d in docs])
		recreate_gl_entries([d.voucher_no for d in docs])
