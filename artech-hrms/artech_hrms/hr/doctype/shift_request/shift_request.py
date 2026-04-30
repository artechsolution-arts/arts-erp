# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import get_link_to_form

import artech_hrms
from artech_hrms.hr.doctype.shift_assignment.shift_assignment import has_overlapping_timings
from artech_hrms.hr.utils import share_doc_with_approver, validate_active_employee
from artech_hrms.mixins.pwa_notifications import PWANotificationsMixin


class OverlappingShiftRequestError(artech_engine.ValidationError):
	pass


class ShiftRequest(Document, PWANotificationsMixin):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amended_from: DF.Link | None
		approver: DF.Link
		company: DF.Link
		department: DF.Link | None
		employee: DF.Link
		employee_name: DF.Data | None
		from_date: DF.Date
		shift_type: DF.Link
		status: DF.Literal["Draft", "Approved", "Rejected"]
		to_date: DF.Date | None
	# end: auto-generated types

	def validate(self):
		validate_active_employee(self.employee)
		self.validate_from_to_dates("from_date", "to_date")
		self.validate_overlapping_shift_requests()
		self.validate_approver()
		self.validate_default_shift()

	def on_update(self):
		share_doc_with_approver(self, self.approver)
		self.notify_approval_status()
		self.publish_update()

	def after_delete(self):
		self.publish_update()

	def publish_update(self):
		employee_user = artech_engine.db.get_value("Employee", self.employee, "user_id", cache=True)
		artech_hrms.refetch_resource("artech_hrms:my_shift_requests", employee_user)
		artech_hrms.refetch_resource("artech_hrms:team_shift_requests")

	def after_insert(self):
		self.notify_approver()

	def on_submit(self):
		if self.status not in ["Approved", "Rejected"]:
			artech_engine.throw(_("Only Shift Request with status 'Approved' and 'Rejected' can be submitted"))
		if self.status == "Approved":
			assignment_doc = artech_engine.new_doc("Shift Assignment")
			assignment_doc.company = self.company
			assignment_doc.shift_type = self.shift_type
			assignment_doc.employee = self.employee
			assignment_doc.start_date = self.from_date
			if self.to_date:
				assignment_doc.end_date = self.to_date
			assignment_doc.shift_request = self.name
			assignment_doc.flags.ignore_permissions = 1
			assignment_doc.insert()
			assignment_doc.submit()

			artech_engine.msgprint(
				_("Shift Assignment: {0} created for Employee: {1}").format(
					artech_engine.bold(assignment_doc.name), artech_engine.bold(self.employee)
				)
			)

	def on_cancel(self):
		shift_assignment_list = artech_engine.db.get_all(
			"Shift Assignment", {"employee": self.employee, "shift_request": self.name, "docstatus": 1}
		)
		if shift_assignment_list:
			for shift in shift_assignment_list:
				shift_assignment_doc = artech_engine.get_doc("Shift Assignment", shift["name"])
				shift_assignment_doc.cancel()

	def on_discard(self):
		self.db_set("status", "Cancelled")

	def validate_default_shift(self):
		default_shift = artech_engine.get_value("Employee", self.employee, "default_shift")
		if self.shift_type == default_shift:
			artech_engine.throw(
				_("You can not request for your Default Shift: {0}").format(artech_engine.bold(self.shift_type))
			)

	def validate_approver(self):
		department = artech_engine.get_value("Employee", self.employee, "department")
		shift_approver = artech_engine.get_value("Employee", self.employee, "shift_request_approver")
		approvers = artech_engine.db.sql(
			"""select approver from `tabDepartment Approver` where parent= %s and parentfield = 'shift_request_approver'""",
			(department),
		)
		approvers = [approver[0] for approver in approvers]
		approvers.append(shift_approver)
		if self.approver not in approvers:
			artech_engine.throw(_("Only Approvers can Approve this Request."))

	def validate_overlapping_shift_requests(self):
		overlapping_dates = self.get_overlapping_dates()
		if len(overlapping_dates):
			# if dates are overlapping, check if timings are overlapping, else allow
			for d in overlapping_dates:
				if has_overlapping_timings(self.shift_type, d.shift_type):
					self.throw_overlap_error(d)

	def get_overlapping_dates(self):
		if not self.name:
			self.name = "New Shift Request"

		shift = artech_engine.qb.DocType("Shift Request")
		query = (
			artech_engine.qb.from_(shift)
			.select(shift.name, shift.shift_type)
			.where(
				(shift.employee == self.employee)
				& (shift.docstatus < 2)
				& (shift.name != self.name)
				& ((shift.to_date >= self.from_date) | (shift.to_date.isnull()))
			)
		)

		if self.to_date:
			query = query.where(shift.from_date <= self.to_date)

		return query.run(as_dict=True)

	def throw_overlap_error(self, shift_details):
		shift_details = artech_engine._dict(shift_details)
		msg = _(
			"Employee {0} has already applied for Shift {1}: {2} that overlaps within this period"
		).format(
			artech_engine.bold(self.employee),
			artech_engine.bold(shift_details.shift_type),
			get_link_to_form("Shift Request", shift_details.name),
		)

		artech_engine.throw(msg, title=_("Overlapping Shift Requests"), exc=OverlappingShiftRequestError)
