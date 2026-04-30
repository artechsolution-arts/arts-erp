# See license.txt

import os

import artech_engine
from artech_engine import _
from artech_engine.core.doctype.user_permission.test_user_permission import create_user
from artech_engine.tests.test_webform import create_custom_doctype, create_webform
from artech_engine.utils import getdate

from artech.setup.doctype.employee.test_employee import make_employee

from artech_hrms.hr.doctype.exit_interview.exit_interview import send_exit_questionnaire
from artech_hrms.tests.utils import HRMSTestSuite


class TestExitInterview(HRMSTestSuite):
	def test_duplicate_interview(self):
		employee = make_employee("employeeexitint1@example.com", company="_Test Company")
		artech_engine.db.set_value("Employee", employee, "relieving_date", getdate())
		interview = create_exit_interview(employee)

		doc = artech_engine.copy_doc(interview)
		self.assertRaises(artech_engine.DuplicateEntryError, doc.save)

	def test_relieving_date_validation(self):
		employee = make_employee("employeeexitint2@example.com", company="_Test Company")
		# unset relieving date
		artech_engine.db.set_value("Employee", employee, "relieving_date", None)

		interview = create_exit_interview(employee, save=False)
		self.assertRaises(artech_engine.ValidationError, interview.save)

		# set relieving date
		artech_engine.db.set_value("Employee", employee, "relieving_date", getdate())
		interview = create_exit_interview(employee)
		self.assertTrue(interview.name)

	def test_interview_date_updated_in_employee_master(self):
		employee = make_employee("employeeexit3@example.com", company="_Test Company")
		artech_engine.db.set_value("Employee", employee, "relieving_date", getdate())

		interview = create_exit_interview(employee)
		interview.status = "Completed"
		interview.employee_status = "Exit Confirmed"

		# exit interview date updated on submit
		interview.submit()
		self.assertEqual(artech_engine.db.get_value("Employee", employee, "held_on"), interview.date)

		# exit interview reset on cancel
		interview.reload()
		interview.cancel()
		self.assertEqual(artech_engine.db.get_value("Employee", employee, "held_on"), None)

	def test_send_exit_questionnaire(self):
		create_custom_doctype()
		create_webform()
		template = create_notification_template()

		webform = artech_engine.db.get_all("Web Form", limit=1)
		artech_engine.db.set_single_value(
			"HR Settings",
			{
				"exit_questionnaire_web_form": webform[0].name,
				"exit_questionnaire_notification_template": template,
			},
		)

		employee = make_employee("employeeexit3@example.com", company="_Test Company")
		artech_engine.db.set_value("Employee", employee, "relieving_date", getdate())

		interview = create_exit_interview(employee)
		send_exit_questionnaire([interview])

		email_queue = artech_engine.db.get_all("Email Queue", ["name", "message"], limit=1)
		self.assertTrue("Subject: Exit Questionnaire Notification" in email_queue[0].message)

	def test_status_on_discard(self):
		employee = make_employee("test_status@example.com", company="_Test Company")
		artech_engine.db.set_value("Employee", employee, "relieving_date", getdate())
		interview = create_exit_interview(employee)
		interview.discard()
		interview.reload()
		self.assertEqual(interview.status, "Cancelled")


def create_exit_interview(employee, save=True):
	interviewer = create_user("test_exit_interviewer@example.com")

	doc = artech_engine.get_doc(
		{
			"doctype": "Exit Interview",
			"employee": employee,
			"company": "_Test Company",
			"status": "Pending",
			"date": getdate(),
			"interviewers": [{"interviewer": interviewer.name}],
			"interview_summary": "Test",
		}
	)

	if save:
		return doc.insert()
	return doc


def create_notification_template():
	template = artech_engine.db.exists("Email Template", _("Exit Questionnaire Notification"))
	if not template:
		base_path = artech_engine.get_app_path("artech", "hr", "doctype")
		response = artech_engine.read_file(
			os.path.join(base_path, "exit_interview/exit_questionnaire_notification_template.html")
		)

		template = artech_engine.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Exit Questionnaire Notification"),
				"response": response,
				"subject": _("Exit Questionnaire Notification"),
				"owner": artech_engine.session.user,
			}
		).insert(ignore_permissions=True)
		template = template.name

	return template
