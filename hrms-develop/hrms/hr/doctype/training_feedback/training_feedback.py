# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class TrainingFeedback(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amended_from: DF.Link | None
		course: DF.Data | None
		department: DF.Link | None
		employee: DF.Link
		employee_name: DF.ReadOnly | None
		event_name: DF.Data | None
		feedback: DF.Text
		trainer_name: DF.Data | None
		training_event: DF.Link
	# end: auto-generated types

	def validate(self):
		training_event = artech_engine.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			artech_engine.throw(_("{0} must be submitted").format(_("Training Event")))

		emp_event_details = artech_engine.db.get_value(
			"Training Event Employee",
			{"parent": self.training_event, "employee": self.employee},
			["name", "attendance"],
			as_dict=True,
		)

		if not emp_event_details:
			artech_engine.throw(
				_("Employee {0} not found in Training Event Participants.").format(
					artech_engine.bold(self.employee_name)
				)
			)

		if emp_event_details.attendance == "Absent":
			artech_engine.throw(_("Feedback cannot be recorded for an absent Employee."))

	def on_submit(self):
		employee = artech_engine.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			artech_engine.db.set_value("Training Event Employee", employee, "status", "Feedback Submitted")

	def on_cancel(self):
		employee = artech_engine.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			artech_engine.db.set_value("Training Event Employee", employee, "status", "Completed")
