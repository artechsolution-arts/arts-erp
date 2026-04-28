import artech_engine
from dateutil.relativedelta import relativedelta
from artech_engine import _, cint
from artech_engine.model.document import Document
from artech_engine.utils import add_days, add_years, cstr, getdate


class FiscalYear(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.accounts.doctype.fiscal_year_company.fiscal_year_company import FiscalYearCompany

		auto_created: DF.Check
		companies: DF.Table[FiscalYearCompany]
		disabled: DF.Check
		is_short_year: DF.Check
		year: DF.Data
		year_end_date: DF.Date
		year_start_date: DF.Date
	# end: auto-generated types

	def validate(self):
		self.validate_dates()
		self.validate_overlap()

	def on_update(self):
		artech_engine.cache().delete_key("fiscal_years")

	def on_trash(self):
		artech_engine.cache().delete_key("fiscal_years")

	def validate_dates(self):
		self.validate_from_to_dates("year_start_date", "year_end_date")
		if self.is_short_year:
			# Fiscal Year can be shorter than one year, in some jurisdictions
			# under certain circumstances. For example, in the USA and Germany.
			return

		date = getdate(self.year_start_date) + relativedelta(years=1) - relativedelta(days=1)

		if getdate(self.year_end_date) != date:
			artech_engine.throw(
				_("Fiscal Year End Date should be one year after Fiscal Year Start Date"),
				artech_engine.exceptions.InvalidDates,
			)

	def validate_overlap(self):
		fy = artech_engine.qb.DocType("Fiscal Year")

		name = self.name or self.year

		existing_fiscal_years = (
			artech_engine.qb.from_(fy)
			.select(fy.name)
			.where(
				(fy.year_start_date <= self.year_end_date)
				& (fy.year_end_date >= self.year_start_date)
				& (fy.name != name)
			)
			.run(as_dict=True)
		)

		if existing_fiscal_years:
			for existing in existing_fiscal_years:
				company_for_existing = artech_engine.db.sql_list(
					"""select company from `tabFiscal Year Company`
					where parent=%s""",
					existing.name,
				)

				overlap = False
				if not self.get("companies") and not company_for_existing:
					overlap = True

				for d in self.get("companies"):
					if d.company in company_for_existing:
						overlap = True

				if overlap:
					artech_engine.throw(
						_(
							"Year start date or end date is overlapping with {0}. To avoid please set company"
						).format(artech_engine.get_desk_link("Fiscal Year", existing.name, open_in_new_tab=True)),
						artech_engine.NameError,
					)


def auto_create_fiscal_year():
	fy = artech_engine.qb.DocType("Fiscal Year")

	# Skipped auto-creating Short Year, as it has very rare use case.
	# Reference: https://www.irs.gov/businesses/small-businesses-self-employed/tax-years (US)
	follow_up_date = add_days(getdate(), days=3)
	fiscal_year = (
		artech_engine.qb.from_(fy)
		.select(fy.name)
		.where((fy.year_end_date == follow_up_date) & (fy.is_short_year == 0))
		.run()
	)

	for d in fiscal_year:
		try:
			current_fy = artech_engine.get_doc("Fiscal Year", d[0])

			new_fy = artech_engine.new_doc("Fiscal Year")
			new_fy.disabled = cint(current_fy.disabled)

			new_fy.year_start_date = add_days(current_fy.year_end_date, 1)
			new_fy.year_end_date = add_years(current_fy.year_end_date, 1)

			start_year = cstr(new_fy.year_start_date.year)
			end_year = cstr(new_fy.year_end_date.year)
			new_fy.year = start_year if start_year == end_year else (start_year + "-" + end_year)

			for row in current_fy.companies:
				new_fy.append("companies", {"company": row.company})

			new_fy.auto_created = 1

			new_fy.insert(ignore_permissions=True)
		except artech_engine.NameError:
			pass


def get_from_and_to_date(fiscal_year):
	fields = ["year_start_date", "year_end_date"]
	cached_results = artech_engine.get_cached_value("Fiscal Year", fiscal_year, fields, as_dict=1)
	return dict(from_date=cached_results.year_start_date, to_date=cached_results.year_end_date)
