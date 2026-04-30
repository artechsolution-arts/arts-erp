# For license information, please see license.txt

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.query_builder.custom import ConstantColumn
from artech_engine.query_builder.functions import Coalesce
from artech_engine.query_builder.terms import SubQuery
from artech_engine.utils import get_link_to_form

from hrms.hr.utils import validate_bulk_tool_fields
from hrms.payroll.doctype.salary_structure.salary_structure import (
	create_salary_structure_assignment,
)


class BulkSalaryStructureAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		branch: DF.Link | None
		company: DF.Link
		currency: DF.Link | None
		department: DF.Link | None
		designation: DF.Link | None
		employment_type: DF.Link | None
		from_date: DF.Date
		grade: DF.Link | None
		income_tax_slab: DF.Link | None
		payroll_payable_account: DF.Link | None
		salary_structure: DF.Link
	# end: auto-generated types

	@artech_engine.whitelist()
	def get_employees(self, advanced_filters: list) -> list:
		quick_filter_fields = [
			"company",
			"employment_type",
			"branch",
			"department",
			"designation",
			"grade",
		]
		filters = [[d, "=", self.get(d)] for d in quick_filter_fields if self.get(d)]
		filters += advanced_filters

		Assignment = artech_engine.qb.DocType("Salary Structure Assignment")
		employees_with_assignments = SubQuery(
			artech_engine.qb.from_(Assignment)
			.select(Assignment.employee)
			.distinct()
			.where((Assignment.from_date == self.from_date) & (Assignment.docstatus == 1))
		)

		Employee = artech_engine.qb.DocType("Employee")
		Grade = artech_engine.qb.DocType("Employee Grade")
		query = (
			artech_engine.qb.get_query(
				Employee,
				fields=[Employee.employee, Employee.employee_name, Employee.grade],
				filters=filters,
			)
			.where(
				(Employee.status == "Active")
				& (Employee.date_of_joining <= self.from_date)
				& ((Employee.relieving_date > self.from_date) | (Employee.relieving_date.isnull()))
				& (Employee.employee.notin(employees_with_assignments))
			)
			.left_join(Grade)
			.on(Employee.grade == Grade.name)
			.select(
				Coalesce(Grade.default_base_pay, 0).as_("base"),
				ConstantColumn(0).as_("variable"),
			)
		)
		return query.run(as_dict=True)

	@artech_engine.whitelist()
	def bulk_assign_structure(self, employees: list) -> None:
		mandatory_fields = ["salary_structure", "from_date", "company"]
		validate_bulk_tool_fields(self, mandatory_fields, employees)

		if len(employees) <= 30:
			return self._bulk_assign_structure(employees)

		artech_engine.enqueue(self._bulk_assign_structure, timeout=3000, employees=employees)
		artech_engine.msgprint(
			_("Creation of Salary Structure Assignments has been queued. It may take a few minutes."),
			alert=True,
			indicator="blue",
		)

	def _bulk_assign_structure(self, employees: list) -> None:
		success, failure = [], []
		count = 0
		savepoint = "before_salary_assignment"

		for d in employees:
			try:
				artech_engine.db.savepoint(savepoint)
				assignment = create_salary_structure_assignment(
					employee=d["employee"],
					salary_structure=self.salary_structure,
					company=self.company,
					currency=self.currency,
					payroll_payable_account=self.payroll_payable_account,
					from_date=self.from_date,
					base=d["base"],
					variable=d["variable"],
					income_tax_slab=self.income_tax_slab,
				)
			except Exception:
				artech_engine.db.rollback(save_point=savepoint)
				artech_engine.log_error(
					f"Bulk Assignment - Salary Structure Assignment failed for employee {d['employee']}.",
					reference_doctype="Salary Structure Assignment",
				)
				failure.append(d["employee"])
			else:
				success.append(
					{
						"doc": get_link_to_form("Salary Structure Assignment", assignment),
						"employee": d["employee"],
					}
				)

			count += 1
			artech_engine.publish_progress(count * 100 / len(employees), title=_("Assigning Structure..."))

		artech_engine.publish_realtime(
			"completed_bulk_salary_structure_assignment",
			message={"success": success, "failure": failure},
			doctype="Bulk Salary Structure Assignment",
			after_commit=True,
		)
