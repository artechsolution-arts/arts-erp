# For license information, please see license.txt

from collections import defaultdict

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.query_builder.functions import Sum
from artech_engine.utils import getdate

from artech import allow_regional
from artech.controllers.accounts_controller import validate_account_head


class TaxWithholdingCategory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.accounts.doctype.tax_withholding_account.tax_withholding_account import (
			TaxWithholdingAccount,
		)
		from artech.accounts.doctype.tax_withholding_rate.tax_withholding_rate import TaxWithholdingRate

		accounts: DF.Table[TaxWithholdingAccount]
		category_name: DF.Data | None
		disable_cumulative_threshold: DF.Check
		disable_transaction_threshold: DF.Check
		rates: DF.Table[TaxWithholdingRate]
		round_off_tax_amount: DF.Check
		tax_deduction_basis: DF.Literal["", "Gross Total", "Net Total"]
		tax_on_excess_amount: DF.Check
	# end: auto-generated types

	def validate(self):
		# TODO: Disable single threshold if tax on excess is enabled
		self.validate_dates()
		self.validate_companies_and_accounts()
		self.validate_thresholds()

	def validate_dates(self):
		group_rates = defaultdict(list)
		for d in self.get("rates"):
			if getdate(d.from_date) >= getdate(d.to_date):
				artech_engine.throw(_("Row #{0}: From Date cannot be before To Date").format(d.idx))
			group_rates[d.tax_withholding_group].append(d)

		# Validate overlapping dates within each group
		for group, rates in group_rates.items():
			rates = sorted(rates, key=lambda d: getdate(d.from_date))
			last_to_date = None

			for d in rates:
				if last_to_date and getdate(d.from_date) < getdate(last_to_date):
					artech_engine.throw(
						_("Row #{0}: Dates overlapping with other row in group {1}").format(
							d.idx, group or "Default"
						)
					)

				last_to_date = d.to_date

	def validate_companies_and_accounts(self):
		existing_accounts = set()
		companies = set()
		for d in self.get("accounts"):
			# validate duplicate company
			if d.get("company") in companies:
				artech_engine.throw(_("Company {0} added multiple times").format(artech_engine.bold(d.get("company"))))
			companies.add(d.get("company"))

			# validate duplicate account
			if d.get("account") in existing_accounts:
				artech_engine.throw(_("Account {0} added multiple times").format(artech_engine.bold(d.get("account"))))

			validate_account_head(d.idx, d.get("account"), d.get("company"))
			existing_accounts.add(d.get("account"))

	def validate_thresholds(self):
		for d in self.get("rates"):
			if d.cumulative_threshold and d.single_threshold and d.cumulative_threshold < d.single_threshold:
				artech_engine.throw(
					_(
						"Row #{0}: Cumulative threshold cannot be less than Single Transaction threshold"
					).format(d.idx)
				)

	def get_applicable_tax_row(self, posting_date, tax_withholding_group):
		for row in self.rates:
			if (
				getdate(row.from_date) <= getdate(posting_date) <= getdate(row.to_date)
				and row.tax_withholding_group == tax_withholding_group
			):
				return row

		artech_engine.throw(_("No Tax Withholding data found for the current posting date."))

	def get_company_account(self, company):
		for row in self.accounts:
			if company == row.company:
				return row.account

		artech_engine.throw(
			_("No Tax withholding account set for Company {0} in Tax Withholding Category {1}.").format(
				artech_engine.bold(company), artech_engine.bold(self.name)
			)
		)


class TaxWithholdingDetails:
	def __init__(
		self,
		tax_withholding_categories: list[str],
		tax_withholding_group: str,
		posting_date: str,
		party_type: str,
		party: str,
		company: str,
	):
		self.tax_withholding_categories = tax_withholding_categories
		self.tax_withholding_group = tax_withholding_group
		self.posting_date = posting_date
		self.party_type = party_type
		self.party = party
		self.company = company
		self.tax_id = get_tax_id_for_party(self.party_type, self.party)

	def get(self) -> list:
		"""
		Fetches tax withholding categories based on the provided parameters.
		"""
		category_details = artech_engine._dict()
		if not self.tax_withholding_categories:
			return category_details

		ldc_details = self.get_ldc_details()

		for category_name in self.tax_withholding_categories:
			doc: TaxWithholdingCategory = artech_engine.get_cached_doc("Tax Withholding Category", category_name)
			row = doc.get_applicable_tax_row(self.posting_date, self.tax_withholding_group)
			account_head = doc.get_company_account(self.company)

			category_detail = artech_engine._dict(
				name=category_name,
				description=doc.category_name,
				account_head=account_head,
				# rates
				tax_rate=row.tax_withholding_rate,
				from_date=row.from_date,
				to_date=row.to_date,
				single_threshold=row.single_threshold,
				cumulative_threshold=row.cumulative_threshold,
				# settings
				tax_deduction_basis=doc.tax_deduction_basis,
				round_off_tax_amount=doc.round_off_tax_amount,
				tax_on_excess_amount=doc.tax_on_excess_amount,
				disable_cumulative_threshold=doc.disable_cumulative_threshold,
				disable_transaction_threshold=doc.disable_transaction_threshold,
				taxable_amount=0,
				tax_id=self.tax_id,
			)

			# ldc (only if valid based on posting date)
			if ldc_detail := ldc_details.get(category_name):
				category_detail.update(ldc_detail)

			category_details[category_name] = category_detail

		return category_details

	def get_ldc_details(self):
		"""
		Fetches the Lower Deduction Certificate (LDC) details for the given party.
		Assumes that only one LDC per category can be valid at a time.
		"""
		ldc_details = {}

		if self.party_type != "Supplier":
			return ldc_details

		# ldc details
		ldc_records = self.get_valid_ldc_records(self.tax_id)
		if not ldc_records:
			return ldc_details

		ldc_names = [ldc.name for ldc in ldc_records]
		ldc_utilization_map = self.get_ldc_utilization_by_category(ldc_names, self.tax_id)

		# map
		for ldc in ldc_records:
			category_name = ldc.tax_withholding_category

			unutilized_amount = ldc.certificate_limit - (ldc_utilization_map.get(ldc.name) or 0)
			if not unutilized_amount:
				continue

			ldc_details[category_name] = dict(
				ldc_certificate=ldc.name,
				ldc_unutilized_amount=unutilized_amount,
				ldc_rate=ldc.rate,
			)

		return ldc_details

	def get_valid_ldc_records(self, tax_id):
		ldc = artech_engine.qb.DocType("Lower Deduction Certificate")
		query = (
			artech_engine.qb.from_(ldc)
			.select(
				ldc.name,
				ldc.tax_withholding_category,
				ldc.rate,
				ldc.certificate_limit,
			)
			.where(
				(ldc.valid_from <= self.posting_date)
				& (ldc.valid_upto >= self.posting_date)
				& (ldc.company == self.company)
				& ldc.tax_withholding_category.isin(self.tax_withholding_categories)
			)
		)

		query = query.where(ldc.pan_no == tax_id) if tax_id else query.where(ldc.supplier == self.party)

		return query.run(as_dict=True)

	def get_ldc_utilization_by_category(self, ldc_names, tax_id):
		twe = artech_engine.qb.DocType("Tax Withholding Entry")
		query = (
			artech_engine.qb.from_(twe)
			.select(twe.lower_deduction_certificate, Sum(twe.taxable_amount).as_("limit_consumed"))
			.where(
				(twe.company == self.company)
				& (twe.party_type == self.party_type)
				& (twe.tax_withholding_category.isin(self.tax_withholding_categories))
				& (twe.lower_deduction_certificate.isin(ldc_names))
				& (twe.docstatus == 1)
				& (twe.status.isin(["Settled", "Over Withheld"]))
			)
			.groupby(twe.lower_deduction_certificate)
		)

		query = query.where(twe.tax_id == tax_id) if tax_id else query.where(twe.party == self.party)

		return artech_engine._dict(query.run())


@allow_regional
def get_tax_id_for_party(party_type, party):
	# cannot use tax_id from doc because payment and journal entry do not have tax_id field.\
	return artech_engine.db.get_value(party_type, party, "tax_id")
