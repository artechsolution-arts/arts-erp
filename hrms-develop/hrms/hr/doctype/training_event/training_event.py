# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import time_diff_in_seconds

from artech.setup.doctype.employee.employee import get_employee_emails


class TrainingEvent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from hrms.hr.doctype.training_event_employee.training_event_employee import TrainingEventEmployee

		amended_from: DF.Link | None
		company: DF.Link | None
		contact_number: DF.Data | None
		course: DF.Data | None
		employee_emails: DF.SmallText | None
		employees: DF.Table[TrainingEventEmployee]
		end_time: DF.Datetime
		event_name: DF.Data
		event_status: DF.Literal["Scheduled", "Completed", "Cancelled"]
		has_certificate: DF.Check
		introduction: DF.TextEditor
		level: DF.Literal["", "Beginner", "Intermediate", "Advance"]
		location: DF.Data
		start_time: DF.Datetime
		supplier: DF.Link | None
		trainer_email: DF.Data | None
		trainer_name: DF.Data | None
		training_program: DF.Link | None
		type: DF.Literal["Seminar", "Theory", "Workshop", "Conference", "Exam", "Internet", "Self-Study"]
	# end: auto-generated types

	def validate(self):
		self.set_employee_emails()
		self.validate_period()

	def on_update_after_submit(self):
		self.set_status_for_attendees()

	def set_employee_emails(self):
		self.employee_emails = ", ".join(get_employee_emails([d.employee for d in self.employees]))

	def validate_period(self):
		if time_diff_in_seconds(self.end_time, self.start_time) <= 0:
			artech_engine.throw(_("End time cannot be before start time"))

	def set_status_for_attendees(self):
		if self.event_status == "Completed":
			for employee in self.employees:
				if employee.attendance == "Present" and employee.status != "Feedback Submitted":
					employee.status = "Completed"

		elif self.event_status == "Scheduled":
			for employee in self.employees:
				employee.status = "Open"

		self.db_update_all()
