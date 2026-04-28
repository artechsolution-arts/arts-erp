import json

import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "purchase_invoice_advance")
	artech_engine.reload_doc("accounts", "doctype", "sales_invoice_advance")

	purchase_invoices = artech_engine.db.sql(
		"""
		select
			parenttype as type, parent as name
		from
			`tabPurchase Invoice Advance`
		where
			ref_exchange_rate = 1
			and docstatus = 1
			and ifnull(exchange_gain_loss, 0) != 0
		group by
			parent
	""",
		as_dict=1,
	)

	sales_invoices = artech_engine.db.sql(
		"""
		select
			parenttype as type, parent as name
		from
			`tabSales Invoice Advance`
		where
			ref_exchange_rate = 1
			and docstatus = 1
			and ifnull(exchange_gain_loss, 0) != 0
		group by
			parent
	""",
		as_dict=1,
	)

	if purchase_invoices + sales_invoices:
		artech_engine.log_error(
			"Fix invalid gain / loss patch log",
			message=json.dumps(purchase_invoices + sales_invoices, indent=2),
		)

	acc_frozen_upto = artech_engine.db.get_single_value("Accounts Settings", "acc_frozen_upto")
	if acc_frozen_upto:
		artech_engine.db.set_single_value("Accounts Settings", "acc_frozen_upto", None)

	for invoice in purchase_invoices + sales_invoices:
		try:
			doc = artech_engine.get_doc(invoice.type, invoice.name)
			doc.docstatus = 2
			doc.make_gl_entries()
			for advance in doc.advances:
				if advance.ref_exchange_rate == 1:
					advance.db_set("exchange_gain_loss", 0, False)
			doc.docstatus = 1
			doc.make_gl_entries()
			artech_engine.db.commit()
		except Exception:
			artech_engine.db.rollback()
			print(f"Failed to correct gl entries of {invoice.name}")

	if acc_frozen_upto:
		artech_engine.db.set_single_value("Accounts Settings", "acc_frozen_upto", acc_frozen_upto)
