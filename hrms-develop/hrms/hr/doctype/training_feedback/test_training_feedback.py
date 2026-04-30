# See license.txt

import artech_engine

from hrms.hr.doctype.training_event.test_training_event import (
	create_training_event,
	create_training_program,
)
from hrms.payroll.doctype.salary_structure.test_salary_structure import make_employee
from hrms.tests.utils import HRMSTestSuite


class TestTrainingFeedback(HRMSTestSuite):
	def setUp(self):
		create_training_program("Basic Training")
		self.employee = make_employee("robert_loan@trainig.com", company="_Test Company")
		self.employee2 = make_employee("suzie.tan@trainig.com", company="_Test Company")
		self.attendees = [{"employee": self.employee}]

	def test_employee_validations_for_feedback(self):
		training_event = create_training_event(self.attendees)
		training_event.submit()

		training_event.event_status = "Completed"
		training_event.save()
		training_event.reload()

		# should not allow creating feedback since employee2 was not part of the event
		feedback = create_training_feedback(training_event.name, self.employee2)
		self.assertRaises(artech_engine.ValidationError, feedback.save)

		# cannot record feedback for absent employee
		employee = artech_engine.db.get_value(
			"Training Event Employee", {"parent": training_event.name, "employee": self.employee}, "name"
		)

		artech_engine.db.set_value("Training Event Employee", employee, "attendance", "Absent")
		feedback = create_training_feedback(training_event.name, self.employee)
		self.assertRaises(artech_engine.ValidationError, feedback.save)

	def test_training_feedback_status(self):
		training_event = create_training_event(self.attendees)
		training_event.submit()

		training_event.event_status = "Completed"
		training_event.save()
		training_event.reload()

		feedback = create_training_feedback(training_event.name, self.employee)
		feedback.submit()

		status = artech_engine.db.get_value(
			"Training Event Employee", {"parent": training_event.name, "employee": self.employee}, "status"
		)

		self.assertEqual(status, "Feedback Submitted")


def create_training_feedback(event, employee):
	return artech_engine.get_doc(
		{
			"doctype": "Training Feedback",
			"training_event": event,
			"employee": employee,
			"feedback": "Test",
		}
	)
