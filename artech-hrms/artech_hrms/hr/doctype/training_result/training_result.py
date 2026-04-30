# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document

from artech.setup.doctype.employee.employee import get_employee_emails


class TrainingResult(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from hrms.hr.doctype.training_result_employee.training_result_employee import TrainingResultEmployee

		amended_from: DF.Link | None
		employee_emails: DF.SmallText | None
		employees: DF.Table[TrainingResultEmployee]
		training_event: DF.Link
	# end: auto-generated types

	def validate(self):
		training_event = artech_engine.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			artech_engine.throw(_("{0} must be submitted").format(_("Training Event")))

		self.employee_emails = ", ".join(get_employee_emails([d.employee for d in self.employees]))

	def on_submit(self):
		training_event = artech_engine.get_doc("Training Event", self.training_event)
		training_event.status = "Completed"
		for e in self.employees:
			for e1 in training_event.employees:
				if e1.employee == e.employee:
					e1.status = "Completed"
					break

		training_event.save()


@artech_engine.whitelist()
def get_employees(training_event: str):
	return artech_engine.get_doc("Training Event", training_event).employees
