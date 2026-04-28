# See license.txt

import artech_engine
from artech_engine import qb
from artech_engine.query_builder.functions import Sum
from artech_engine.utils import add_days, nowdate, today

from artech.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from artech.accounts.doctype.payment_request.payment_request import make_payment_request
from artech.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from artech.accounts.utils import get_fiscal_year
from artech.stock.doctype.item.test_item import make_item
from artech.stock.doctype.purchase_receipt.test_purchase_receipt import get_gl_entries, make_purchase_receipt
from artech.tests.utils import ArtechTestSuite


class TestRepostAccountingLedger(ArtechTestSuite):
	def setUp(self):
		artech_engine.db.set_single_value("Selling Settings", "validate_selling_price", 0)
		update_repost_settings()

	def test_01_basic_functions(self):
		si = create_sales_invoice(
			item="_Test Item",
			company="_Test Company",
			customer="_Test Customer",
			debit_to="Debtors - _TC",
			parent_cost_center="Main - _TC",
			cost_center="Main - _TC",
			rate=100,
		)

		preq = artech_engine.get_doc(
			make_payment_request(
				dt=si.doctype,
				dn=si.name,
				payment_request_type="Inward",
				party_type="Customer",
				party=si.customer,
			)
		)
		preq.save().submit()

		# Test Validation Error
		ral = artech_engine.new_doc("Repost Accounting Ledger")
		ral.company = "_Test Company"
		ral.delete_cancelled_entries = True
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		ral.append(
			"vouchers", {"voucher_type": preq.doctype, "voucher_no": preq.name}
		)  # this should throw validation error
		self.assertRaises(artech_engine.ValidationError, ral.save)
		ral.vouchers.pop()
		preq.cancel()
		preq.delete()

		pe = get_payment_entry(si.doctype, si.name)
		pe.save().submit()
		ral.append("vouchers", {"voucher_type": pe.doctype, "voucher_no": pe.name})
		ral.save()

		# manually set an incorrect debit amount in DB
		gle = artech_engine.db.get_all("GL Entry", filters={"voucher_no": si.name, "account": "Debtors - _TC"})
		artech_engine.db.set_value("GL Entry", gle[0], "debit", 90)

		gl = qb.DocType("GL Entry")
		res = (
			qb.from_(gl)
			.select(gl.voucher_no, Sum(gl.debit).as_("debit"), Sum(gl.credit).as_("credit"))
			.where((gl.voucher_no == si.name) & (gl.is_cancelled == 0))
			.run()
		)

		# Assert incorrect ledger balance
		self.assertNotEqual(res[0], (si.name, 100, 100))

		# Submit repost document
		ral.save().submit()

		res = (
			qb.from_(gl)
			.select(gl.voucher_no, Sum(gl.debit).as_("debit"), Sum(gl.credit).as_("credit"))
			.where((gl.voucher_no == si.name) & (gl.is_cancelled == 0))
			.run()
		)

		# Ledger should reflect correct amount post repost
		self.assertEqual(res[0], (si.name, 100, 100))

	def test_02_deferred_accounting_valiations(self):
		si = create_sales_invoice(
			item="_Test Item",
			company="_Test Company",
			customer="_Test Customer",
			debit_to="Debtors - _TC",
			parent_cost_center="Main - _TC",
			cost_center="Main - _TC",
			rate=100,
			do_not_submit=True,
		)
		si.items[0].enable_deferred_revenue = True
		si.items[0].deferred_revenue_account = "Deferred Revenue - _TC"
		si.items[0].service_start_date = nowdate()
		si.items[0].service_end_date = add_days(nowdate(), 90)
		si.save().submit()

		ral = artech_engine.new_doc("Repost Accounting Ledger")
		ral.company = "_Test Company"
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		self.assertRaises(artech_engine.ValidationError, ral.save)

	@ArtechTestSuite.change_settings("Accounts Settings", {"delete_linked_ledger_entries": 1})
	def test_04_pcv_validation(self):
		# Clear old GL entries so PCV can be submitted.
		gl = artech_engine.qb.DocType("GL Entry")
		qb.from_(gl).delete().where(gl.company == "_Test Company").run()

		si = create_sales_invoice(
			item="_Test Item",
			company="_Test Company",
			customer="_Test Customer",
			debit_to="Debtors - _TC",
			parent_cost_center="Main - _TC",
			cost_center="Main - _TC",
			rate=100,
		)
		fy = get_fiscal_year(today(), company="_Test Company")
		pcv = artech_engine.get_doc(
			{
				"doctype": "Period Closing Voucher",
				"transaction_date": today(),
				"period_start_date": fy[1],
				"period_end_date": today(),
				"company": "_Test Company",
				"fiscal_year": fy[0],
				"cost_center": "Main - _TC",
				"closing_account_head": "Retained Earnings - _TC",
				"remarks": "test",
			}
		)
		pcv.save().submit()

		ral = artech_engine.new_doc("Repost Accounting Ledger")
		ral.company = "_Test Company"
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		self.assertRaises(artech_engine.ValidationError, ral.save)

		pcv.reload()
		pcv.cancel()
		pcv.delete()

	def test_03_deletion_flag_and_preview_function(self):
		si = create_sales_invoice(
			item="_Test Item",
			company="_Test Company",
			customer="_Test Customer",
			debit_to="Debtors - _TC",
			parent_cost_center="Main - _TC",
			cost_center="Main - _TC",
			rate=100,
		)

		pe = get_payment_entry(si.doctype, si.name)
		pe.save().submit()

		# with deletion flag set
		ral = artech_engine.new_doc("Repost Accounting Ledger")
		ral.company = "_Test Company"
		ral.delete_cancelled_entries = True
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		ral.append("vouchers", {"voucher_type": pe.doctype, "voucher_no": pe.name})
		ral.save().submit()

		self.assertIsNone(artech_engine.db.exists("GL Entry", {"voucher_no": si.name, "is_cancelled": 1}))
		self.assertIsNone(artech_engine.db.exists("GL Entry", {"voucher_no": pe.name, "is_cancelled": 1}))

	def test_05_without_deletion_flag(self):
		si = create_sales_invoice(
			item="_Test Item",
			company="_Test Company",
			customer="_Test Customer",
			debit_to="Debtors - _TC",
			parent_cost_center="Main - _TC",
			cost_center="Main - _TC",
			rate=100,
		)

		pe = get_payment_entry(si.doctype, si.name)
		pe.save().submit()

		# without deletion flag set
		ral = artech_engine.new_doc("Repost Accounting Ledger")
		ral.company = "_Test Company"
		ral.delete_cancelled_entries = False
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		ral.append("vouchers", {"voucher_type": pe.doctype, "voucher_no": pe.name})
		ral.save().submit()

		self.assertIsNotNone(artech_engine.db.exists("GL Entry", {"voucher_no": si.name, "is_cancelled": 1}))
		self.assertIsNotNone(artech_engine.db.exists("GL Entry", {"voucher_no": pe.name, "is_cancelled": 1}))

	def test_06_repost_purchase_receipt(self):
		from artech.accounts.doctype.account.test_account import create_account

		if not artech_engine.db.set_value("Company", "_Test Company", "service_expense_account"):
			artech_engine.db.set_value(
				"Company", "_Test Company", "service_expense_account", "Marketing Expenses - _TC"
			)

		provisional_account = create_account(
			account_name="Provision Account",
			parent_account="Current Liabilities - _TC",
			company="_Test Company",
		)

		another_provisional_account = create_account(
			account_name="Another Provision Account",
			parent_account="Current Liabilities - _TC",
			company="_Test Company",
		)

		company = artech_engine.get_doc("Company", "_Test Company")
		company.enable_provisional_accounting_for_non_stock_items = 1
		company.default_provisional_account = provisional_account
		company.save()

		test_cc = company.cost_center
		default_expense_account = company.service_expense_account

		item = make_item(properties={"is_stock_item": 0})

		pr = make_purchase_receipt(company="_Test Company", item_code=item.name, rate=1000.0, qty=1.0)
		pr_gl_entries = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
		expected_pr_gles = [
			{"account": provisional_account, "debit": 0.0, "credit": 1000.0, "cost_center": test_cc},
			{"account": default_expense_account, "debit": 1000.0, "credit": 0.0, "cost_center": test_cc},
		]
		self.assertEqual(expected_pr_gles, pr_gl_entries)

		# change the provisional account
		artech_engine.db.set_value(
			"Purchase Receipt Item",
			pr.items[0].name,
			"provisional_expense_account",
			another_provisional_account,
		)

		repost_doc = artech_engine.new_doc("Repost Accounting Ledger")
		repost_doc.company = "_Test Company"
		repost_doc.delete_cancelled_entries = True
		repost_doc.append("vouchers", {"voucher_type": pr.doctype, "voucher_no": pr.name})
		repost_doc.save().submit()

		pr_gles_after_repost = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
		expected_pr_gles_after_repost = [
			{"account": default_expense_account, "debit": 1000.0, "credit": 0.0, "cost_center": test_cc},
			{"account": another_provisional_account, "debit": 0.0, "credit": 1000.0, "cost_center": test_cc},
		]
		self.assertEqual(len(pr_gles_after_repost), len(expected_pr_gles_after_repost))
		self.assertEqual(expected_pr_gles_after_repost, pr_gles_after_repost)

		# teardown
		repost_doc.cancel()
		repost_doc.delete()

		pr.reload()
		pr.cancel()

		company.enable_provisional_accounting_for_non_stock_items = 0
		company.default_provisional_account = None
		company.save()


def update_repost_settings():
	allowed_types = [
		"Sales Invoice",
		"Purchase Invoice",
		"Payment Entry",
		"Journal Entry",
		"Purchase Receipt",
	]
	settings = artech_engine.get_doc("Accounts Settings")
	for _type in allowed_types:
		if _type not in [x.document_type for x in settings.repost_allowed_types]:
			settings.append("repost_allowed_types", {"document_type": _type})
	settings.save()
