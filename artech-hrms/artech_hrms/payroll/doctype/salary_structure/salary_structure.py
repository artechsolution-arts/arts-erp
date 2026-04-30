import datetime
import re

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.model.mapper import get_mapped_doc
from artech_engine.utils import cint, cstr, flt, get_link_to_form

import artech

from artech_hrms.payroll.utils import sanitize_expression


class SalaryStructure(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.payroll.doctype.employee_benefit_detail.employee_benefit_detail import EmployeeBenefitDetail
		from artech_hrms.payroll.doctype.salary_detail.salary_detail import SalaryDetail

		amended_from: DF.Link | None
		company: DF.Link
		currency: DF.Link
		deductions: DF.Table[SalaryDetail]
		earnings: DF.Table[SalaryDetail]
		employee_benefits: DF.Table[EmployeeBenefitDetail]
		hour_rate: DF.Currency
		is_active: DF.Literal["", "Yes", "No"]
		is_default: DF.Literal["Yes", "No"]
		leave_encashment_amount_per_day: DF.Currency
		letter_head: DF.Link | None
		max_benefits: DF.Currency
		mode_of_payment: DF.Link | None
		net_pay: DF.Currency
		payment_account: DF.Link | None
		payroll_frequency: DF.Literal["", "Monthly", "Fortnightly", "Bimonthly", "Weekly", "Daily"]
		salary_component: DF.Link | None
		salary_slip_based_on_timesheet: DF.Check
		total_deduction: DF.Currency
		total_earning: DF.Currency
	# end: auto-generated types

	def before_validate(self):
		self.sanitize_condition_and_formula_fields()

	def before_update_after_submit(self):
		self.sanitize_condition_and_formula_fields()

	def validate(self):
		self.set_missing_values()
		self.validate_amount()
		self.validate_component_based_on_tax_slab()
		self.validate_payment_days_based_dependent_component()
		self.validate_timesheet_component()
		self.validate_formula_setup()
		validate_max_benefit_for_flexible_benefit(self.employee_benefits, self.max_benefits)

	def on_update(self):
		self.reset_condition_and_formula_fields()

	def on_update_after_submit(self):
		self.reset_condition_and_formula_fields()

	def validate_formula_setup(self):
		for table in ["earnings", "deductions"]:
			for row in self.get(table):
				if not row.amount_based_on_formula and row.formula:
					artech_engine.msgprint(
						_(
							"{0} Row #{1}: Formula is set but {2} is disabled for the Salary Component {3}."
						).format(
							table.capitalize(),
							row.idx,
							artech_engine.bold(_("Amount Based on Formula")),
							artech_engine.bold(row.salary_component),
						),
						title=_("Warning"),
						indicator="orange",
					)

	def set_missing_values(self):
		overwritten_fields = [
			"depends_on_payment_days",
			"variable_based_on_taxable_salary",
			"is_tax_applicable",
			"is_flexible_benefit",
		]
		overwritten_fields_if_missing = ["amount_based_on_formula", "formula", "amount"]
		for table in ["earnings", "deductions"]:
			for d in self.get(table):
				component_default_value = artech_engine.db.get_value(
					"Salary Component",
					cstr(d.salary_component),
					overwritten_fields + overwritten_fields_if_missing,
					as_dict=1,
				)
				if component_default_value:
					for fieldname in overwritten_fields:
						value = component_default_value.get(fieldname)
						if d.get(fieldname) != value:
							d.set(fieldname, value)

					if not (d.get("amount") or d.get("formula")):
						for fieldname in overwritten_fields_if_missing:
							d.set(fieldname, component_default_value.get(fieldname))

	def validate_component_based_on_tax_slab(self):
		for row in self.deductions:
			if row.variable_based_on_taxable_salary and (row.amount or row.formula):
				artech_engine.throw(
					_(
						"Row #{0}: Cannot set amount or formula for Salary Component {1} with Variable Based On Taxable Salary"
					).format(row.idx, row.salary_component)
				)

	def validate_amount(self):
		if flt(self.net_pay) < 0 and self.salary_slip_based_on_timesheet:
			artech_engine.throw(_("Net pay cannot be negative"))

	def validate_payment_days_based_dependent_component(self):
		abbreviations = self.get_component_abbreviations()
		for component_type in ("earnings", "deductions"):
			for row in self.get(component_type):
				if (
					row.formula
					and row.depends_on_payment_days
					# check if the formula contains any of the payment days components
					and any(re.search(r"\b" + abbr + r"\b", row.formula) for abbr in abbreviations)
				):
					message = _("Row #{0}: The {1} Component has the options {2} and {3} enabled.").format(
						row.idx,
						artech_engine.bold(row.salary_component),
						artech_engine.bold(_("Amount based on formula")),
						artech_engine.bold(_("Depends On Payment Days")),
					)
					message += "<br><br>" + _(
						"Disable {0} for the {1} component, to prevent the amount from being deducted twice, as its formula already uses a payment-days-based component."
					).format(artech_engine.bold(_("Depends On Payment Days")), artech_engine.bold(row.salary_component))
					artech_engine.throw(message, title=_("Payment Days Dependency"))

	def get_component_abbreviations(self):
		abbr = [d.abbr for d in self.earnings if d.depends_on_payment_days]
		abbr += [d.abbr for d in self.deductions if d.depends_on_payment_days]

		return abbr

	def validate_timesheet_component(self):
		if not self.salary_slip_based_on_timesheet:
			return

		for component in self.earnings:
			if component.salary_component == self.salary_component:
				artech_engine.msgprint(
					_(
						"Row #{0}: Timesheet amount will overwrite the Earning component amount for the Salary Component {1}"
					).format(self.idx, artech_engine.bold(self.salary_component)),
					title=_("Warning"),
					indicator="orange",
				)
				break

	def sanitize_condition_and_formula_fields(self):
		for table in ("earnings", "deductions"):
			for row in self.get(table):
				row.condition = row.condition.strip() if row.condition else ""
				row.formula = row.formula.strip() if row.formula else ""
				row._condition, row.condition = row.condition, sanitize_expression(row.condition)
				row._formula, row.formula = row.formula, sanitize_expression(row.formula)

	def reset_condition_and_formula_fields(self):
		# set old values (allowing multiline strings for better readability in the doctype form)
		for table in ("earnings", "deductions"):
			for row in self.get(table):
				row.condition = row._condition
				row.formula = row._formula

		self.db_update_all()

	def get_employees(self, **kwargs):
		conditions, values = [], []
		for field, value in kwargs.items():
			if value:
				conditions.append(f"{field}=%s")
				values.append(value)

		condition_str = " and " + " and ".join(conditions) if conditions else ""

		# nosemgrep: frappe-semgrep-rules.rules.frappe-using-db-sql
		employees = artech_engine.db.sql_list(
			f"select name from tabEmployee where status='Active' {condition_str}",
			tuple(values),
		)

		return employees

	@artech_engine.whitelist()
	def assign_salary_structure(
		self,
		branch: str | None = None,
		grade: str | None = None,
		department: str | None = None,
		designation: str | None = None,
		employee: str | None = None,
		payroll_payable_account: str | None = None,
		from_date: str | None = None,
		base: float | None = None,
		variable: float | None = None,
		income_tax_slab: str | None = None,
	) -> None:
		employees = self.get_employees(
			company=self.company,
			grade=grade,
			department=department,
			designation=designation,
			name=employee,
			branch=branch,
		)

		if employees:
			if len(employees) > 20:
				artech_engine.enqueue(
					assign_salary_structure_for_employees,
					timeout=3000,
					employees=employees,
					salary_structure=self,
					payroll_payable_account=payroll_payable_account,
					from_date=from_date,
					base=base,
					variable=variable,
					income_tax_slab=income_tax_slab,
				)
			else:
				assign_salary_structure_for_employees(
					employees,
					self,
					payroll_payable_account=payroll_payable_account,
					from_date=from_date,
					base=base,
					variable=variable,
					income_tax_slab=income_tax_slab,
				)
		else:
			artech_engine.msgprint(_("No Employee Found"))


def assign_salary_structure_for_employees(
	employees,
	salary_structure,
	payroll_payable_account=None,
	from_date=None,
	base=None,
	variable=None,
	income_tax_slab=None,
):
	assignments = []
	existing_assignments_for = get_existing_assignments(employees, salary_structure, from_date)
	count = 0
	savepoint = "before_assignment_submission"

	for employee in employees:
		try:
			artech_engine.db.savepoint(savepoint)
			if employee in existing_assignments_for:
				continue

			count += 1

			assignment = create_salary_structure_assignment(
				employee,
				salary_structure.name,
				salary_structure.company,
				salary_structure.currency,
				from_date,
				payroll_payable_account,
				base,
				variable,
				income_tax_slab,
			)
			assignments.append(assignment)
			artech_engine.publish_progress(
				count * 100 / len(set(employees) - set(existing_assignments_for)),
				title=_("Assigning Structures..."),
			)
		except Exception:
			artech_engine.db.rollback(save_point=savepoint)
			artech_engine.log_error(
				f"Salary Structure Assignment failed for employee {employee}",
				reference_doctype="Salary Structure Assignment",
			)

	if assignments:
		artech_engine.msgprint(_("Structures have been assigned successfully"))


def create_salary_structure_assignment(
	employee,
	salary_structure,
	company,
	currency,
	from_date,
	payroll_payable_account=None,
	base=None,
	variable=None,
	income_tax_slab=None,
):
	assignment = artech_engine.new_doc("Salary Structure Assignment")

	if not payroll_payable_account:
		payroll_payable_account = artech_engine.db.get_value("Company", company, "default_payroll_payable_account")
		if not payroll_payable_account:
			artech_engine.throw(_('Please set "Default Payroll Payable Account" in Company Defaults'))

	payroll_payable_account_currency = artech_engine.db.get_value(
		"Account", payroll_payable_account, "account_currency"
	)
	company_curency = artech.get_company_currency(company)
	if payroll_payable_account_currency != currency and payroll_payable_account_currency != company_curency:
		artech_engine.throw(
			_("Invalid Payroll Payable Account. The account currency must be {0} or {1}").format(
				currency, company_curency
			)
		)

	assignment.employee = employee
	assignment.salary_structure = salary_structure
	assignment.company = company
	assignment.currency = currency
	assignment.payroll_payable_account = payroll_payable_account
	assignment.from_date = from_date
	assignment.base = base
	assignment.variable = variable
	assignment.income_tax_slab = income_tax_slab
	assignment.save(ignore_permissions=True)
	assignment.submit()

	return assignment.name


def get_existing_assignments(employees, salary_structure, from_date):
	# nosemgrep: frappe-semgrep-rules.rules.frappe-using-db-sql
	salary_structures_assignments = artech_engine.db.sql_list(
		f"""
		SELECT DISTINCT employee FROM `tabSalary Structure Assignment`
		WHERE salary_structure=%s AND employee IN ({", ".join(["%s"] * len(employees))})
		AND from_date=%s AND company=%s AND docstatus=1
		""",
		[salary_structure.name, *employees, from_date, salary_structure.company],
	)
	if salary_structures_assignments:
		artech_engine.msgprint(
			_(
				"Skipping Salary Structure Assignment for the following employees, as Salary Structure Assignment records already exists against them. {0}"
			).format("\n".join(salary_structures_assignments))
		)
	return salary_structures_assignments


@artech_engine.whitelist()
def make_salary_slip(
	source_name: str,
	target_doc: str | Document | None = None,
	employee: str | None = None,
	posting_date: str | datetime.date | None = None,
	as_print: bool = False,
	print_format: str | None = None,
	for_preview: int = 0,
	ignore_permissions: bool = False,
	lwp_days_corrected: float | None = None,
) -> str | Document:
	def postprocess(source, target):
		if employee:
			target.employee = employee
			if posting_date:
				target.posting_date = posting_date

		target.run_method(
			"process_salary_structure", for_preview=for_preview, lwp_days_corrected=lwp_days_corrected
		)

	doc = get_mapped_doc(
		"Salary Structure",
		source_name,
		{
			"Salary Structure": {
				"doctype": "Salary Slip",
				"field_map": {
					"total_earning": "gross_pay",
					"name": "salary_structure",
					"currency": "currency",
				},
			}
		},
		target_doc,
		postprocess,
		ignore_child_tables=True,
		ignore_permissions=ignore_permissions,
		cached=True,
	)

	if cint(as_print):
		doc.name = f"Preview for {employee}"
		return artech_engine.get_print(doc.doctype, doc.name, doc=doc, print_format=print_format)
	else:
		return doc


@artech_engine.whitelist()
def get_employees(salary_structure: str) -> list[str]:
	employees = artech_engine.get_list(
		"Salary Structure Assignment",
		filters={"salary_structure": salary_structure, "docstatus": 1},
		pluck="employee",
	)

	if not employees:
		artech_engine.throw(
			_(
				"There's no Employee with Salary Structure: {0}. Assign {1} to an Employee to preview Salary Slip"
			).format(salary_structure, salary_structure)
		)

	return list(set(employees))


@artech_engine.whitelist()
def get_salary_component(
	doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict
) -> list:
	sc = artech_engine.qb.DocType("Salary Component")
	sca = artech_engine.qb.DocType("Salary Component Account")

	salary_components = (
		artech_engine.qb.from_(sc)
		.left_join(sca)
		.on(sca.parent == sc.name)
		.select(sc.name, sca.account, sca.company)
		.where(
			(sc.type == filters.get("component_type"))
			& (sc.disabled == 0)
			& (sc[searchfield].like(f"%{txt}%") | sc.name.like(f"%{txt}%"))
		)
		.limit(page_len)
		.offset(start)
	).run(as_dict=True)

	accounts = []
	for component in salary_components:
		if not component.company:
			accounts.append((component.name, component.account, component.company))
		else:
			if component.company == filters["company"]:
				accounts.append((component.name, component.account, component.company))

	return accounts


def validate_max_benefit_for_flexible_benefit(employee_benefits, max_benefits=None):
	if not employee_benefits:
		return

	benefit_total = 0
	benefit_components = []

	for benefit in employee_benefits:
		if benefit.salary_component in benefit_components:
			artech_engine.throw(
				_("Salary Component {0} cannot be selected more than once in Employee Benefits").format(
					benefit.salary_component
				)
			)

		benefit_total += benefit.amount
		max_of_component = artech_engine.db.get_value(
			"Salary Component", benefit.salary_component, "max_benefit_amount"
		)
		if max_of_component and max_of_component > 0 and benefit.amount > max_of_component:
			artech_engine.throw(
				_(
					"Benefit amount {0} for Salary Component {1} should not be greater than maximum benefit amount {2} set in {3}"
				).format(
					benefit.amount,
					benefit.salary_component,
					max_of_component,
					get_link_to_form("Salary Component", benefit.salary_component),
				)
			)
		benefit_components.append(benefit.salary_component)

	if max_benefits and benefit_total > max_benefits:
		artech_engine.throw(
			_("Total of all employee benefits cannot be greater that Max Benefits Amount {0}").format(
				max_benefits
			),
			title=_("Invalid Benefit Amounts"),
		)
