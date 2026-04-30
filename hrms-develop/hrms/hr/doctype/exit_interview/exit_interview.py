# For license information, please see license.txt

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import get_link_to_form

from artech.setup.doctype.employee.employee import get_employee_email


class ExitInterview(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from hrms.hr.doctype.interviewer.interviewer import Interviewer

		amended_from: DF.Link | None
		company: DF.Link
		date: DF.Date | None
		date_of_joining: DF.Date | None
		department: DF.Link | None
		designation: DF.Link | None
		email: DF.Data | None
		employee: DF.Link
		employee_name: DF.Data | None
		employee_status: DF.Literal["", "Employee Retained", "Exit Confirmed"]
		interview_summary: DF.TextEditor | None
		interviewers: DF.TableMultiSelect[Interviewer]
		naming_series: DF.Literal["HR-EXIT-INT-"]
		questionnaire_email_sent: DF.Check
		ref_doctype: DF.Link | None
		reference_document_name: DF.DynamicLink | None
		relieving_date: DF.Date | None
		reports_to: DF.Link | None
		status: DF.Literal["Pending", "Scheduled", "Completed", "Cancelled"]
	# end: auto-generated types

	def validate(self):
		self.validate_relieving_date()
		self.validate_duplicate_interview()
		self.set_employee_email()

	def validate_relieving_date(self):
		if not artech_engine.db.get_value("Employee", self.employee, "relieving_date"):
			artech_engine.throw(
				_("Please set the relieving date for employee {0}").format(
					get_link_to_form("Employee", self.employee)
				),
				title=_("Relieving Date Missing"),
			)

	def validate_duplicate_interview(self):
		doc = artech_engine.db.exists(
			"Exit Interview", {"employee": self.employee, "name": ("!=", self.name), "docstatus": ("!=", 2)}
		)
		if doc:
			artech_engine.throw(
				_("Exit Interview {0} already exists for Employee: {1}").format(
					get_link_to_form("Exit Interview", doc), artech_engine.bold(self.employee)
				),
				artech_engine.DuplicateEntryError,
			)

	def set_employee_email(self):
		employee = artech_engine.get_doc("Employee", self.employee)
		self.email = get_employee_email(employee)

	def on_submit(self):
		if self.status != "Completed":
			artech_engine.throw(_("Only Completed documents can be submitted"))

		self.update_interview_date_in_employee()

	def on_cancel(self):
		self.update_interview_date_in_employee()
		self.db_set("status", "Cancelled")

	def on_discard(self):
		self.db_set("status", "Cancelled")

	def update_interview_date_in_employee(self):
		if self.docstatus == 1:
			artech_engine.db.set_value("Employee", self.employee, "held_on", self.date)
		elif self.docstatus == 2:
			artech_engine.db.set_value("Employee", self.employee, "held_on", None)


@artech_engine.whitelist()
def send_exit_questionnaire(interviews: str | list) -> None:
	interviews = get_interviews(interviews)
	validate_questionnaire_settings()

	email_success = []
	email_failure = []

	for exit_interview in interviews:
		interview = artech_engine.get_doc("Exit Interview", exit_interview.get("name"))
		if interview.get("questionnaire_email_sent"):
			continue

		employee = artech_engine.get_doc("Employee", interview.employee)
		email = get_employee_email(employee)

		context = interview.as_dict()
		context.update(employee.as_dict())
		template_name = artech_engine.db.get_single_value("HR Settings", "exit_questionnaire_notification_template")
		template = artech_engine.get_doc("Email Template", template_name)

		if email:
			artech_engine.sendmail(
				recipients=email,
				subject=template.subject,
				message=artech_engine.render_template(template.response, context),
				reference_doctype=interview.doctype,
				reference_name=interview.name,
			)
			interview.db_set("questionnaire_email_sent", 1)
			interview.notify_update()
			email_success.append(email)
		else:
			email_failure.append(get_link_to_form("Employee", employee.name))

	show_email_summary(email_success, email_failure)


def get_interviews(interviews):
	import json

	if isinstance(interviews, str):
		interviews = json.loads(interviews)

	if not len(interviews):
		artech_engine.throw(_("At least one interview has to be selected."))

	return interviews


def validate_questionnaire_settings():
	settings = artech_engine.db.get_value(
		"HR Settings",
		"HR Settings",
		["exit_questionnaire_web_form", "exit_questionnaire_notification_template"],
		as_dict=True,
	)

	if not settings.exit_questionnaire_web_form or not settings.exit_questionnaire_notification_template:
		artech_engine.throw(
			_("Please set {0} and {1} in {2}.").format(
				artech_engine.bold(_("Exit Questionnaire Web Form")),
				artech_engine.bold(_("Notification Template")),
				get_link_to_form("HR Settings", "HR Settings"),
			),
			title=_("Settings Missing"),
		)


def show_email_summary(email_success, email_failure):
	message = ""
	if email_success:
		message += _("Sent Successfully: {0}").format(", ".join(email_success))
	if message and email_failure:
		message += "<br><br>"
	if email_failure:
		message += _("Sending Failed due to missing email information for employee(s): {1}").format(
			", ".join(email_failure)
		)

	artech_engine.msgprint(message, title=_("Exit Questionnaire"), indicator="blue", is_minimizable=True, wide=True)
