# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import artech_engine
from artech_engine.utils import nowdate

from artech.accounts.doctype.account.account import (
	InvalidAccountMergeError,
	merge_account,
	update_account_number,
)
from artech.stock import get_company_default_inventory_account, get_warehouse_account
from artech.tests.utils import ArtechTestSuite


class TestAccount(ArtechTestSuite):
	def test_rename_account(self):
		if not artech_engine.db.exists("Account", "1210 - Debtors - _TC"):
			acc = artech_engine.new_doc("Account")
			acc.account_name = "Debtors"
			acc.parent_account = "Accounts Receivable - _TC"
			acc.account_number = "1210"
			acc.company = "_Test Company"
			acc.insert()

		account_number, account_name = artech_engine.db.get_value(
			"Account", "1210 - Debtors - _TC", ["account_number", "account_name"]
		)
		self.assertEqual(account_number, "1210")
		self.assertEqual(account_name, "Debtors")

		new_account_number = "1211-11-4 - 6 - "
		new_account_name = "Debtors 1 - Test - "

		update_account_number("1210 - Debtors - _TC", new_account_name, new_account_number)

		new_acc = artech_engine.db.get_value(
			"Account",
			"1211-11-4 - 6 - - Debtors 1 - Test - - _TC",
			["account_name", "account_number"],
			as_dict=1,
		)

		self.assertEqual(new_acc.account_name, "Debtors 1 - Test -")
		self.assertEqual(new_acc.account_number, "1211-11-4 - 6 -")

		artech_engine.delete_doc("Account", "1211-11-4 - 6 - Debtors 1 - Test - - _TC")

	def test_merge_account(self):
		create_account(
			account_name="Current Assets",
			is_group=1,
			parent_account="Application of Funds (Assets) - _TC",
			company="_Test Company",
		)

		create_account(
			account_name="Securities and Deposits",
			is_group=1,
			parent_account="Current Assets - _TC",
			company="_Test Company",
		)

		create_account(
			account_name="Earnest Money",
			parent_account="Securities and Deposits - _TC",
			company="_Test Company",
		)

		create_account(
			account_name="Cash In Hand",
			is_group=1,
			parent_account="Current Assets - _TC",
			company="_Test Company",
		)

		create_account(
			account_name="Receivable INR",
			parent_account="Current Assets - _TC",
			company="_Test Company",
			account_currency="INR",
		)

		create_account(
			account_name="Receivable USD",
			parent_account="Current Assets - _TC",
			company="_Test Company",
			account_currency="USD",
		)

		parent = artech_engine.db.get_value("Account", "Earnest Money - _TC", "parent_account")

		self.assertEqual(parent, "Securities and Deposits - _TC")

		merge_account("Securities and Deposits - _TC", "Cash In Hand - _TC")

		parent = artech_engine.db.get_value("Account", "Earnest Money - _TC", "parent_account")

		# Parent account of the child account changes after merging
		self.assertEqual(parent, "Cash In Hand - _TC")

		# Old account doesn't exist after merging
		self.assertFalse(artech_engine.db.exists("Account", "Securities and Deposits - _TC"))

		# Raise error as is_group property doesn't match
		self.assertRaises(
			InvalidAccountMergeError,
			merge_account,
			"Current Assets - _TC",
			"Accumulated Depreciation - _TC",
		)

		# Raise error as root_type property doesn't match
		self.assertRaises(
			InvalidAccountMergeError,
			merge_account,
			"Capital Stock - _TC",
			"Software - _TC",
		)

		# Raise error as currency doesn't match
		self.assertRaises(
			InvalidAccountMergeError,
			merge_account,
			"Receivable INR - _TC",
			"Receivable USD - _TC",
		)

	def test_account_sync(self):
		artech_engine.local.flags.pop("ignore_root_company_validation", None)

		acc = artech_engine.new_doc("Account")
		acc.account_name = "Test Sync Account"
		acc.parent_account = "Temporary Accounts - _TC3"
		acc.company = "_Test Company 3"
		acc.insert()

		acc_tc_4 = artech_engine.db.get_value(
			"Account", {"account_name": "Test Sync Account", "company": "_Test Company 4"}
		)
		acc_tc_5 = artech_engine.db.get_value(
			"Account", {"account_name": "Test Sync Account", "company": "_Test Company 5"}
		)
		self.assertEqual(acc_tc_4, "Test Sync Account - _TC4")
		self.assertEqual(acc_tc_5, "Test Sync Account - _TC5")

	def test_add_account_to_a_group(self):
		artech_engine.db.set_value("Account", "Office Rent - _TC3", "is_group", 1)

		acc = artech_engine.new_doc("Account")
		acc.account_name = "Test Group Account"
		acc.parent_account = "Office Rent - _TC3"
		acc.company = "_Test Company 3"
		self.assertRaises(artech_engine.ValidationError, acc.insert)

		artech_engine.db.set_value("Account", "Office Rent - _TC3", "is_group", 0)

	def test_account_rename_sync(self):
		artech_engine.local.flags.pop("ignore_root_company_validation", None)

		acc = artech_engine.new_doc("Account")
		acc.account_name = "Test Rename Account"
		acc.parent_account = "Temporary Accounts - _TC3"
		acc.company = "_Test Company 3"
		acc.insert()

		# Rename account in parent company
		update_account_number(acc.name, "Test Rename Sync Account", "1234")

		# Check if renamed in children
		self.assertTrue(
			artech_engine.db.exists(
				"Account",
				{
					"account_name": "Test Rename Sync Account",
					"company": "_Test Company 4",
					"account_number": "1234",
				},
			)
		)
		self.assertTrue(
			artech_engine.db.exists(
				"Account",
				{
					"account_name": "Test Rename Sync Account",
					"company": "_Test Company 5",
					"account_number": "1234",
				},
			)
		)

		artech_engine.delete_doc("Account", "1234 - Test Rename Sync Account - _TC3")
		artech_engine.delete_doc("Account", "1234 - Test Rename Sync Account - _TC4")
		artech_engine.delete_doc("Account", "1234 - Test Rename Sync Account - _TC5")

	def test_account_currency_sync(self):
		"""
		In a parent->child company setup, child should inherit parent account currency if explicitly specified.
		"""

		artech_engine.local.flags.pop("ignore_root_company_validation", None)

		def create_bank_account():
			acc = artech_engine.new_doc("Account")
			acc.account_name = "_Test Bank JPY"

			acc.parent_account = "Temporary Accounts - _TC6"
			acc.company = "_Test Company 6"
			return acc

		acc = create_bank_account()
		# Explicitly set currency
		acc.account_currency = "JPY"
		acc.insert()
		self.assertTrue(
			artech_engine.db.exists(
				{
					"doctype": "Account",
					"account_name": "_Test Bank JPY",
					"account_currency": "JPY",
					"company": "_Test Company 7",
				}
			)
		)

		artech_engine.delete_doc("Account", "_Test Bank JPY - _TC6")
		artech_engine.delete_doc("Account", "_Test Bank JPY - _TC7")

		acc = create_bank_account()
		# default currency is used
		acc.insert()
		self.assertTrue(
			artech_engine.db.exists(
				{
					"doctype": "Account",
					"account_name": "_Test Bank JPY",
					"account_currency": "USD",
					"company": "_Test Company 7",
				}
			)
		)

		artech_engine.delete_doc("Account", "_Test Bank JPY - _TC6")
		artech_engine.delete_doc("Account", "_Test Bank JPY - _TC7")

	def test_child_company_account_rename_sync(self):
		artech_engine.local.flags.pop("ignore_root_company_validation", None)

		acc = artech_engine.new_doc("Account")
		acc.account_name = "Test Group Account"
		acc.parent_account = "Temporary Accounts - _TC3"
		acc.is_group = 1
		acc.company = "_Test Company 3"
		acc.insert()

		self.assertTrue(
			artech_engine.db.exists("Account", {"account_name": "Test Group Account", "company": "_Test Company 4"})
		)
		self.assertTrue(
			artech_engine.db.exists("Account", {"account_name": "Test Group Account", "company": "_Test Company 5"})
		)

		# Try renaming child company account
		acc_tc_5 = artech_engine.db.get_value(
			"Account", {"account_name": "Test Group Account", "company": "_Test Company 5"}
		)
		self.assertRaises(artech_engine.ValidationError, update_account_number, acc_tc_5, "Test Modified Account")

		# Rename child company account with allow_account_creation_against_child_company enabled
		artech_engine.db.set_value("Company", "_Test Company 5", "allow_account_creation_against_child_company", 1)

		update_account_number(acc_tc_5, "Test Modified Account")
		self.assertTrue(
			artech_engine.db.exists(
				"Account", {"name": "Test Modified Account - _TC5", "company": "_Test Company 5"}
			)
		)

		artech_engine.db.set_value("Company", "_Test Company 5", "allow_account_creation_against_child_company", 0)

		to_delete = [
			"Test Group Account - _TC3",
			"Test Group Account - _TC4",
			"Test Modified Account - _TC5",
		]
		for doc in to_delete:
			artech_engine.delete_doc("Account", doc)

	def test_validate_account_currency(self):
		from artech.accounts.doctype.journal_entry.test_journal_entry import make_journal_entry

		if not artech_engine.db.get_value("Account", "Test Currency Account - _TC"):
			acc = artech_engine.new_doc("Account")
			acc.account_name = "Test Currency Account"
			acc.parent_account = "Tax Assets - _TC"
			acc.company = "_Test Company"
			acc.insert()
		else:
			acc = artech_engine.get_doc("Account", "Test Currency Account - _TC")

		self.assertEqual(acc.account_currency, "INR")

		# Make a JV against this account
		make_journal_entry("Test Currency Account - _TC", "Miscellaneous Expenses - _TC", 100, submit=True)

		acc.account_currency = "USD"
		self.assertRaises(artech_engine.ValidationError, acc.save)

	def test_account_balance(self):
		from artech.accounts.utils import get_balance_on

		if not artech_engine.db.exists("Account", "Test Percent Account %5 - _TC"):
			acc = artech_engine.new_doc("Account")
			acc.account_name = "Test Percent Account %5"
			acc.parent_account = "Tax Assets - _TC"
			acc.company = "_Test Company"
			acc.insert()

		balance = get_balance_on(account="Test Percent Account %5 - _TC", date=nowdate())
		self.assertEqual(balance, 0)


def get_inventory_account(company, warehouse=None):
	account = None
	if warehouse:
		account = get_warehouse_account(artech_engine.get_doc("Warehouse", warehouse))
	else:
		account = get_company_default_inventory_account(company)

	return account


def create_account(**kwargs):
	account = artech_engine.db.get_value(
		"Account", filters={"account_name": kwargs.get("account_name"), "company": kwargs.get("company")}
	)
	if account:
		account = artech_engine.get_doc("Account", account)
		account.update(
			dict(
				is_group=kwargs.get("is_group", 0),
				parent_account=kwargs.get("parent_account"),
			)
		)
		account.save()
		return account.name
	else:
		account = artech_engine.get_doc(
			doctype="Account",
			is_group=kwargs.get("is_group", 0),
			account_name=kwargs.get("account_name"),
			account_type=kwargs.get("account_type"),
			parent_account=kwargs.get("parent_account"),
			company=kwargs.get("company"),
			account_currency=kwargs.get("account_currency"),
		)

		account.save()
		return account.name
