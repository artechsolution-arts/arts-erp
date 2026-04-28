# Copyright (c) 2015, Artech and Contributors
import json

import artech_engine
from artech_engine import _
from artech_engine.utils import random_string

from artech.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
	get_charts_for_country,
)
from artech.setup.doctype.company.company import get_default_company_address
from artech.tests.utils import ArtechTestSuite


class TestCompany(ArtechTestSuite):
	def test_coa_based_on_existing_company(self):
		company = artech_engine.new_doc("Company")
		company.company_name = "COA from Existing Company"
		company.abbr = "CFEC"
		company.default_currency = "INR"
		company.create_chart_of_accounts_based_on = "Existing Company"
		company.existing_company = "_Test Company"
		company.country = "India"
		company.save()

		expected_results = {
			"Debtors - CFEC": {
				"account_type": "Receivable",
				"is_group": 0,
				"root_type": "Asset",
				"parent_account": "Accounts Receivable - CFEC",
			},
			"Cash - CFEC": {
				"account_type": "Cash",
				"is_group": 0,
				"root_type": "Asset",
				"parent_account": "Cash In Hand - CFEC",
			},
		}

		for account, acc_property in expected_results.items():
			acc = artech_engine.get_doc("Account", account)
			for prop, val in acc_property.items():
				self.assertEqual(acc.get(prop), val)

		artech_engine.delete_doc("Company", "COA from Existing Company")

	def test_coa_based_on_country_template(self):
		countries = ["Canada", "Germany", "France"]

		for country in countries:
			templates = get_charts_for_country(country)
			if len(templates) != 1 and "Standard" in templates:
				templates.remove("Standard")

			self.assertTrue(templates)

			for company in artech_engine.db.get_all("Company", {"company_name": ["in", templates]}):
				artech_engine.delete_doc("Company", company.name)

			for template in templates:
				try:
					company = artech_engine.new_doc("Company")
					company.company_name = template
					company.abbr = random_string(3)
					company.default_currency = "USD"
					company.create_chart_of_accounts_based_on = "Standard Template"
					company.chart_of_accounts = template
					company.country = country
					company.save()

					account_types = [
						"Cost of Goods Sold",
						"Depreciation",
						"Expenses Included In Valuation",
						"Fixed Asset",
						"Payable",
						"Receivable",
						"Stock Adjustment",
						"Stock Received But Not Billed",
						"Bank",
						"Cash",
						"Stock",
					]

					for account_type in account_types:
						filters = {"company": template, "account_type": account_type}
						if account_type in ["Bank", "Cash"]:
							filters["is_group"] = 1

						has_matching_accounts = artech_engine.get_all("Account", filters)
						error_message = _("No Account matched these filters: {}").format(json.dumps(filters))

						self.assertTrue(has_matching_accounts, msg=error_message)
				finally:
					artech_engine.delete_doc("Company", template)

	def test_basic_tree(self, records=None):
		self.load_test_records("Company")
		min_lft = 1
		max_rgt = artech_engine.db.sql("select max(rgt) from `tabCompany`")[0][0]

		if not records:
			records = self.globalTestRecords["Company"][2:]

		for company in records:
			lft, rgt, parent_company = artech_engine.db.get_value(
				"Company", company.get("company_name"), ["lft", "rgt", "parent_company"]
			)

			if parent_company:
				parent_lft, parent_rgt = artech_engine.db.get_value("Company", parent_company, ["lft", "rgt"])
			else:
				# root
				parent_lft = min_lft - 1
				parent_rgt = max_rgt + 1

			self.assertTrue(lft)
			self.assertTrue(rgt)
			self.assertTrue(lft < rgt)
			self.assertTrue(parent_lft < parent_rgt)
			self.assertTrue(lft > parent_lft)
			self.assertTrue(rgt < parent_rgt)
			self.assertTrue(lft >= min_lft)
			self.assertTrue(rgt <= max_rgt)

	def test_primary_address(self):
		company = "_Test Company"

		secondary = artech_engine.get_doc(
			{
				"address_title": "Non Primary",
				"doctype": "Address",
				"address_type": "Billing",
				"address_line1": "Something",
				"city": "Mumbai",
				"state": "Maharashtra",
				"country": "India",
				"is_primary_address": 1,
				"pincode": "400098",
				"links": [
					{
						"link_doctype": "Company",
						"link_name": company,
					}
				],
			}
		)
		secondary.insert()
		self.addCleanup(secondary.delete)

		primary = artech_engine.copy_doc(secondary)
		primary.is_primary_address = 1
		primary.insert()
		self.addCleanup(primary.delete)

		self.assertEqual(get_default_company_address(company), primary.name)

	def get_no_of_children(self, company):
		def get_no_of_children(companies, no_of_children):
			children = []
			for company in companies:
				children += artech_engine.db.sql_list(
					"""select name from `tabCompany`
				where ifnull(parent_company, '')=%s""",
					company or "",
				)

			if len(children):
				return get_no_of_children(children, no_of_children + len(children))
			else:
				return no_of_children

		return get_no_of_children([company], 0)

	def test_change_parent_company(self):
		child_company = artech_engine.get_doc("Company", "_Test Company 5")

		# changing parent of company
		child_company.parent_company = "_Test Company 3"
		child_company.save()
		self.test_basic_tree()

		# move it back
		child_company.parent_company = "_Test Company 4"
		child_company.save()
		self.test_basic_tree()

	def test_demo_data(self):
		from artech.setup.demo import clear_demo_data, setup_demo_data

		self.load_test_records("Company")

		setup_demo_data(self.globalTestRecords["Company"][0]["company_name"])
		company_name = artech_engine.db.get_value("Company", {"name": ("like", "%(Demo)")})
		self.assertTrue(company_name)

		for transaction in artech_engine.get_hooks("demo_transaction_doctypes"):
			self.assertTrue(artech_engine.db.exists(artech_engine.unscrub(transaction), {"company": company_name}))

		clear_demo_data()
		company_name = artech_engine.db.get_value("Company", {"name": ("like", "%(Demo)")})
		self.assertFalse(company_name)
		for transaction in artech_engine.get_hooks("demo_transaction_doctypes"):
			self.assertFalse(artech_engine.db.exists(artech_engine.unscrub(transaction), {"company": company_name}))


def create_company_communication(doctype, docname):
	comm = artech_engine.get_doc(
		{
			"doctype": "Communication",
			"communication_type": "Communication",
			"content": "Deduplication of Links",
			"communication_medium": "Email",
			"reference_doctype": doctype,
			"reference_name": docname,
		}
	)
	comm.insert()


def create_child_company():
	child_company = artech_engine.db.exists("Company", "Test Company")
	if not child_company:
		child_company = artech_engine.get_doc(
			{
				"doctype": "Company",
				"company_name": "Test Company",
				"abbr": "test_company",
				"default_currency": "INR",
			}
		)
		child_company.insert()
	else:
		child_company = artech_engine.get_doc("Company", child_company)

	return child_company.name


def create_test_lead_in_company(company):
	lead = artech_engine.db.exists("Lead", "Test Lead in new company")
	if not lead:
		lead = artech_engine.get_doc(
			{"doctype": "Lead", "lead_name": "Test Lead in new company", "scompany": company}
		)
		lead.insert()
	else:
		lead = artech_engine.get_doc("Lead", lead)
		lead.company = company
		lead.save()
	return lead.name
