# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.model.mapper import get_mapped_doc

from artech_hrms.controllers.employee_boarding_controller import EmployeeBoardingController


class IncompleteTaskError(artech_engine.ValidationError):
	pass


class EmployeeOnboarding(EmployeeBoardingController):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.hr.doctype.employee_boarding_activity.employee_boarding_activity import (
			EmployeeBoardingActivity,
		)

		activities: DF.Table[EmployeeBoardingActivity]
		amended_from: DF.Link | None
		boarding_begins_on: DF.Date
		boarding_status: DF.Literal["Pending", "In Process", "Completed"]
		company: DF.Link
		date_of_joining: DF.Date
		department: DF.Link | None
		designation: DF.Link | None
		employee: DF.Link | None
		employee_grade: DF.Link | None
		employee_name: DF.Data
		employee_onboarding_template: DF.Link | None
		holiday_list: DF.Link | None
		job_applicant: DF.Link
		job_offer: DF.Link
		notify_users_by_email: DF.Check
		project: DF.Link | None
	# end: auto-generated types

	def validate(self):
		super().validate()
		self.set_employee()
		self.validate_duplicate_employee_onboarding()

	def set_employee(self):
		if not self.employee:
			self.employee = artech_engine.db.get_value("Employee", {"job_applicant": self.job_applicant}, "name")

	def validate_duplicate_employee_onboarding(self):
		emp_onboarding = artech_engine.db.exists(
			"Employee Onboarding", {"job_applicant": self.job_applicant, "docstatus": ("!=", 2)}
		)
		if emp_onboarding and emp_onboarding != self.name:
			artech_engine.throw(
				_("Employee Onboarding: {0} already exists for Job Applicant: {1}").format(
					artech_engine.bold(emp_onboarding), artech_engine.bold(self.job_applicant)
				)
			)

	def validate_employee_creation(self):
		if self.docstatus != 1:
			artech_engine.throw(_("Submit this to create the Employee record"))
		else:
			for activity in self.activities:
				if not activity.required_for_employee_creation:
					continue
				else:
					task_status = artech_engine.db.get_value("Task", activity.task, "status")
					if task_status not in ["Completed", "Cancelled"]:
						artech_engine.throw(
							_("All the mandatory tasks for employee creation are not completed yet."),
							IncompleteTaskError,
						)

	def on_submit(self):
		super().on_submit()

	def on_update_after_submit(self):
		self.create_task_and_notify_user()

	def on_cancel(self):
		super().on_cancel()

	@artech_engine.whitelist()
	def mark_onboarding_as_completed(self):
		for activity in self.activities:
			artech_engine.db.set_value("Task", activity.task, "status", "Completed")
		artech_engine.db.set_value("Project", self.project, "status", "Completed")
		self.boarding_status = "Completed"
		self.save()


@artech_engine.whitelist()
def make_employee(source_name: str, target_doc: str | Document | None = None) -> Document:
	doc = artech_engine.get_doc("Employee Onboarding", source_name)
	doc.validate_employee_creation()

	def set_missing_values(source, target):
		target.personal_email = artech_engine.db.get_value("Job Applicant", source.job_applicant, "email_id")
		target.status = "Active"

	doc = get_mapped_doc(
		"Employee Onboarding",
		source_name,
		{
			"Employee Onboarding": {
				"doctype": "Employee",
				"field_map": {
					"first_name": "employee_name",
					"employee_grade": "grade",
				},
			}
		},
		target_doc,
		set_missing_values,
	)
	return doc
