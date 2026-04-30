# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document
from artech_engine.utils import format_date

# Wether to proceed with frequency change
PROCEED_WITH_FREQUENCY_CHANGE = False


class HRSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		allow_employee_checkin_from_mobile_app: DF.Check
		allow_geolocation_tracking: DF.Check
		allow_multiple_shift_assignments: DF.Check
		auto_leave_encashment: DF.Check
		check_vacancies: DF.Check
		emp_created_by: DF.Literal["Naming Series", "Employee Number", "Full Name"]
		exit_questionnaire_notification_template: DF.Link | None
		exit_questionnaire_web_form: DF.Link | None
		expense_approver_mandatory_in_expense_claim: DF.Check
		feedback_reminder_notification_template: DF.Link | None
		frequency: DF.Literal["Weekly", "Monthly"]
		hiring_sender: DF.Link | None
		hiring_sender_email: DF.Data | None
		interview_reminder_template: DF.Link | None
		leave_approval_notification_template: DF.Link | None
		leave_approver_mandatory_in_leave_application: DF.Check
		leave_status_notification_template: DF.Link | None
		prevent_self_expense_approval: DF.Check
		prevent_self_leave_approval: DF.Check
		remind_before: DF.Time | None
		restrict_backdated_leave_application: DF.Check
		retirement_age: DF.Data | None
		role_allowed_to_create_backdated_leave_application: DF.Link | None
		send_birthday_reminders: DF.Check
		send_holiday_reminders: DF.Check
		send_interview_feedback_reminder: DF.Check
		send_interview_reminder: DF.Check
		send_leave_notification: DF.Check
		send_work_anniversary_reminders: DF.Check
		sender: DF.Link | None
		sender_email: DF.Data | None
		show_leaves_of_all_department_members_in_calendar: DF.Check
		standard_working_hours: DF.Float
		unlink_payment_on_cancellation_of_employee_advance: DF.Check
	# end: auto-generated types

	def validate(self):
		self.set_naming_series()

		# Based on proceed flag
		global PROCEED_WITH_FREQUENCY_CHANGE
		if not PROCEED_WITH_FREQUENCY_CHANGE:
			self.validate_frequency_change()
		PROCEED_WITH_FREQUENCY_CHANGE = False

	def set_naming_series(self):
		from artech.utilities.naming import set_by_naming_series

		set_by_naming_series(
			"Employee",
			"employee_number",
			self.get("emp_created_by") == "Naming Series",
			hide_name_field=True,
		)

	def validate_frequency_change(self):
		weekly_job, monthly_job = None, None

		try:
			weekly_job = artech_engine.get_doc(
				"Scheduled Job Type",
				{"method": "hrms.controllers.employee_reminders.send_reminders_in_advance_weekly"},
			)

			monthly_job = artech_engine.get_doc(
				"Scheduled Job Type",
				{"method": "hrms.controllers.employee_reminders.send_reminders_in_advance_monthly"},
			)
		except artech_engine.DoesNotExistError:
			return

		next_weekly_trigger = weekly_job.get_next_execution()
		next_monthly_trigger = monthly_job.get_next_execution()

		if self.freq_changed_from_monthly_to_weekly():
			if next_monthly_trigger < next_weekly_trigger:
				self.show_freq_change_warning(next_monthly_trigger, next_weekly_trigger)

		elif self.freq_changed_from_weekly_to_monthly():
			if next_monthly_trigger > next_weekly_trigger:
				self.show_freq_change_warning(next_weekly_trigger, next_monthly_trigger)

	def freq_changed_from_weekly_to_monthly(self):
		return self.has_value_changed("frequency") and self.frequency == "Monthly"

	def freq_changed_from_monthly_to_weekly(self):
		return self.has_value_changed("frequency") and self.frequency == "Weekly"

	def show_freq_change_warning(self, from_date, to_date):
		from_date = artech_engine.bold(format_date(from_date))
		to_date = artech_engine.bold(format_date(to_date))

		raise_exception = artech_engine.ValidationError
		if (
			artech_engine.flags.in_test
			or artech_engine.flags.in_patch
			or artech_engine.flags.in_install
			or artech_engine.flags.in_migrate
		):
			raise_exception = False

		artech_engine.msgprint(
			msg=artech_engine._(
				"Employees will miss holiday reminders from {} until {}. <br> Do you want to proceed with this change?"
			).format(from_date, to_date),
			title="Confirm change in Frequency",
			primary_action={
				"label": artech_engine._("Yes, Proceed"),
				"client_action": "hrms.proceed_save_with_reminders_frequency_change",
			},
			raise_exception=raise_exception,
		)


@artech_engine.whitelist()
def set_proceed_with_frequency_change():
	"""Enables proceed with frequency change"""
	global PROCEED_WITH_FREQUENCY_CHANGE
	PROCEED_WITH_FREQUENCY_CHANGE = True
