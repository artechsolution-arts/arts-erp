from datetime import date

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.query_builder.terms import ValueWrapper
from artech_engine.utils import (
	add_days,
	cint,
	create_batch,
	cstr,
	format_date,
	get_datetime,
	get_link_to_form,
	getdate,
	nowdate,
)
from artech_engine.utils.background_jobs import get_job

import artech_hrms
from artech_hrms.hr.doctype.shift_assignment.shift_assignment import has_overlapping_timings
from artech_hrms.hr.utils import (
	get_holidays_for_employee,
	validate_active_employee,
)
from artech_hrms.utils.holiday_list import get_holiday_dates_between_range


class DuplicateAttendanceError(artech_engine.ValidationError):
	pass


class OverlappingShiftAttendanceError(artech_engine.ValidationError):
	pass


class Attendance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		actual_overtime_duration: DF.Float
		amended_from: DF.Link | None
		attendance_date: DF.Date
		attendance_request: DF.Link | None
		company: DF.Link
		department: DF.Link | None
		early_exit: DF.Check
		employee: DF.Link
		employee_name: DF.Data | None
		half_day_status: DF.Literal["", "Present", "Absent"]
		in_time: DF.Datetime | None
		late_entry: DF.Check
		leave_application: DF.Link | None
		leave_type: DF.Link | None
		modify_half_day_status: DF.Check
		naming_series: DF.Literal["HR-ATT-.YYYY.-"]
		out_time: DF.Datetime | None
		overtime_type: DF.Link | None
		shift: DF.Link | None
		standard_working_hours: DF.Float
		status: DF.Literal["", "Present", "Absent", "On Leave", "Half Day", "Work From Home"]
		working_hours: DF.Float
	# end: auto-generated types

	def before_insert(self):
		if self.half_day_status == "":
			self.half_day_status = None

	def validate(self):
		from artech.controllers.status_updater import validate_status

		validate_status(self.status, ["Present", "Absent", "On Leave", "Half Day", "Work From Home"])
		validate_active_employee(self.employee)
		self.validate_attendance_date()
		self.validate_duplicate_record()
		self.validate_overlapping_shift_attendance()
		self.validate_employee_status()
		self.check_leave_record()

	def on_cancel(self):
		self.unlink_attendance_from_checkins()

	def validate_attendance_date(self):
		date_of_joining = artech_engine.db.get_value("Employee", self.employee, "date_of_joining")

		if date_of_joining and getdate(self.attendance_date) < getdate(date_of_joining):
			artech_engine.throw(
				_("Attendance date {0} can not be less than employee {1}'s joining date: {2}").format(
					artech_engine.bold(format_date(self.attendance_date)),
					artech_engine.bold(self.employee),
					artech_engine.bold(format_date(date_of_joining)),
				)
			)

	def validate_duplicate_record(self):
		duplicate = self.get_duplicate_attendance_record()

		if duplicate:
			artech_engine.throw(
				_("Attendance for employee {0} is already marked for the date {1}: {2}").format(
					artech_engine.bold(self.employee),
					artech_engine.bold(format_date(self.attendance_date)),
					get_link_to_form("Attendance", duplicate),
				),
				title=_("Duplicate Attendance"),
				exc=DuplicateAttendanceError,
			)

	def get_duplicate_attendance_record(self) -> str | None:
		Attendance = artech_engine.qb.DocType("Attendance")
		query = (
			artech_engine.qb.from_(Attendance)
			.select(Attendance.name)
			.where(
				(Attendance.employee == self.employee)
				& (Attendance.docstatus < 2)
				& (Attendance.attendance_date == self.attendance_date)
				& (Attendance.name != self.name)
				& (
					Attendance.half_day_status.isnull()
					| (Attendance.half_day_status == "")
					| (Attendance.modify_half_day_status == 0)
				)
			)
			.for_update()
		)

		if self.shift:
			query = query.where(
				((Attendance.shift.isnull()) | (Attendance.shift == ""))
				| (
					((Attendance.shift.isnotnull()) | (Attendance.shift != ""))
					& (Attendance.shift == self.shift)
				)
			)

		duplicate = query.run(pluck=True)

		return duplicate[0] if duplicate else None

	def validate_overlapping_shift_attendance(self):
		attendance = self.get_overlapping_shift_attendance()

		if attendance:
			artech_engine.throw(
				_("Attendance for employee {0} is already marked for an overlapping shift {1}: {2}").format(
					artech_engine.bold(self.employee),
					artech_engine.bold(attendance.shift),
					get_link_to_form("Attendance", attendance.name),
				),
				title=_("Overlapping Shift Attendance"),
				exc=OverlappingShiftAttendanceError,
			)

	def get_overlapping_shift_attendance(self) -> dict:
		if not self.shift:
			return {}

		Attendance = artech_engine.qb.DocType("Attendance")
		same_date_attendance = (
			artech_engine.qb.from_(Attendance)
			.select(Attendance.name, Attendance.shift)
			.where(
				(Attendance.employee == self.employee)
				& (Attendance.docstatus < 2)
				& (Attendance.attendance_date == self.attendance_date)
				& (Attendance.shift != self.shift)
				& (Attendance.name != self.name)
			)
		).run(as_dict=True)

		for d in same_date_attendance:
			if has_overlapping_timings(self.shift, d.shift):
				return d

		return {}

	def validate_employee_status(self):
		if artech_engine.db.get_value("Employee", self.employee, "status") == "Inactive":
			artech_engine.throw(_("Cannot mark attendance for an Inactive employee {0}").format(self.employee))

	def check_leave_record(self):
		LeaveApplication = artech_engine.qb.DocType("Leave Application")
		leave_record = (
			artech_engine.qb.from_(LeaveApplication)
			.select(
				LeaveApplication.leave_type,
				LeaveApplication.half_day,
				LeaveApplication.half_day_date,
				LeaveApplication.name,
			)
			.where(
				(LeaveApplication.employee == self.employee)
				& (self.attendance_date >= LeaveApplication.from_date)
				& (self.attendance_date <= LeaveApplication.to_date)
				& (LeaveApplication.status == "Approved")
				& (LeaveApplication.docstatus == 1)
			)
		).run(as_dict=True)

		if leave_record:
			for d in leave_record:
				self.leave_type = d.leave_type
				self.leave_application = d.name
				if d.half_day_date == getdate(self.attendance_date):
					self.status = "Half Day"
					artech_engine.msgprint(
						_("Employee {0} on Half day on {1}").format(
							self.employee, format_date(self.attendance_date)
						)
					)
				else:
					self.status = "On Leave"
					artech_engine.msgprint(
						_("Employee {0} is on Leave on {1}").format(
							self.employee, format_date(self.attendance_date)
						)
					)

		if self.status in ("On Leave", "Half Day"):
			if not leave_record:
				self.modify_half_day_status = 0
				self.half_day_status = "Absent"
				artech_engine.msgprint(
					_("No leave record found for employee {0} on {1}").format(
						self.employee, format_date(self.attendance_date)
					),
					alert=1,
				)
		elif self.leave_type:
			self.leave_type = None
			self.leave_application = None

	def validate_employee(self):
		emp = artech_engine.db.sql(
			"select name from `tabEmployee` where name = %s and status = 'Active'", self.employee
		)
		if not emp:
			artech_engine.throw(_("Employee {0} is not active or does not exist").format(self.employee))

	def unlink_attendance_from_checkins(self):
		EmployeeCheckin = artech_engine.qb.DocType("Employee Checkin")
		linked_logs = (
			artech_engine.qb.from_(EmployeeCheckin)
			.select(EmployeeCheckin.name)
			.where(EmployeeCheckin.attendance == self.name)
			.for_update()
			.run(as_dict=True)
		)

		if linked_logs:
			(
				artech_engine.qb.update(EmployeeCheckin)
				.set("attendance", "")
				.where(EmployeeCheckin.attendance == self.name)
			).run()

			artech_engine.msgprint(
				msg=_("Unlinked Attendance record from Employee Checkins: {}").format(
					", ".join(get_link_to_form("Employee Checkin", log.name) for log in linked_logs)
				),
				title=_("Unlinked logs"),
				indicator="blue",
				is_minimizable=True,
				wide=True,
			)

	def on_update(self):
		self.publish_update()

	def after_delete(self):
		self.publish_update()

	def publish_update(self):
		employee_user = artech_engine.db.get_value("Employee", self.employee, "user_id", cache=True)
		artech_hrms.refetch_resource("artech_hrms:attendance_calendar_events", employee_user)


@artech_engine.whitelist()
def get_events(start: date | str, end: date | str, filters: str | list | None = None) -> list[dict]:
	employee = artech_engine.db.get_value("Employee", {"user_id": artech_engine.session.user})
	if not employee:
		return []

	if isinstance(filters, str):
		import json

		filters = json.loads(filters)
	if not filters:
		filters = []
	filters.append(["attendance_date", "between", [get_datetime(start).date(), get_datetime(end).date()]])
	attendance_records = add_attendance(filters)
	add_holidays(attendance_records, start, end, employee)
	return attendance_records


def add_attendance(filters):
	attendance = artech_engine.get_list(
		"Attendance",
		fields=[
			"name",
			ValueWrapper("Attendance").as_("doctype"),
			"attendance_date",
			"employee_name",
			"status",
			"docstatus",
		],
		filters=filters,
	)
	for record in attendance:
		record["title"] = f"{record['employee_name']} : {record['status']}"
	return attendance


def add_holidays(events, start, end, employee=None):
	holidays = get_holidays_for_employee(employee, start, end)
	if not holidays:
		return

	for holiday in holidays:
		events.append(
			{
				"doctype": "Holiday",
				"attendance_date": holiday.holiday_date,
				"title": _("Holiday") + ": " + cstr(holiday.description),
				"name": holiday.name,
				"allDay": 1,
			}
		)


def mark_attendance(
	employee,
	attendance_date,
	status,
	shift=None,
	leave_type=None,
	late_entry=False,
	early_exit=False,
	half_day_status=None,
):
	savepoint = "attendance_creation"

	try:
		artech_engine.db.savepoint(savepoint)
		attendance = artech_engine.new_doc("Attendance")
		attendance.update(
			{
				"doctype": "Attendance",
				"employee": employee,
				"attendance_date": attendance_date,
				"status": status,
				"shift": shift,
				"leave_type": leave_type,
				"late_entry": late_entry,
				"early_exit": early_exit,
				"half_day_status": half_day_status,
			}
		)
		attendance.insert()
		attendance.submit()
	except (DuplicateAttendanceError, OverlappingShiftAttendanceError):
		artech_engine.db.rollback(save_point=savepoint)
		return

	return attendance.name


@artech_engine.whitelist()
def mark_bulk_attendance(data: str | dict):
	import json

	if isinstance(data, str):
		data = json.loads(data)
	data = artech_engine._dict(data)
	if not data.unmarked_days:
		artech_engine.throw(_("Please select a date."))
		return
	if len(data.unmarked_days) > 10 or artech_engine.flags.test_bg_job:
		job_id = f"process_bulk_attendance_for_employee_{data.employee}"
		job = artech_engine.enqueue(
			process_bulk_attendance_in_batches, data=data, job_id=job_id, timeout=600, deduplicate=True
		)
		if job:
			message = _(
				"Bulk attendance marking is queued with a background job. It may take a while. You can monitor the job status {0}"
			).format(get_link_to_form("RQ Job", job.id, label="here"))
		else:
			message = _(
				"Bulk attendance marking is already in progress for employee {0}. You can monitor the job status {1}"
			).format(artech_engine.bold(data.employee), get_link_to_form("RQ Job", get_job(job_id).id, label="here"))
		artech_engine.msgprint(message, allow_dangerous_html=True)
	else:
		process_bulk_attendance_in_batches(data)
		artech_engine.msgprint(_("Attendance marked successfully."), alert=True)


def process_bulk_attendance_in_batches(data, chunk_size=20):
	savepoint = "mark_bulk_attendance"
	for days in create_batch(data.unmarked_days, chunk_size):
		for attendance_date in days:
			try:
				artech_engine.db.savepoint(savepoint)
				doc_dict = {
					"doctype": "Attendance",
					"employee": data.employee,
					"attendance_date": getdate(attendance_date),
					"status": data.status,
					"half_day_status": "Absent" if data.status == "Half Day" else None,
					"shift": data.shift,
				}
				attendance = artech_engine.get_doc(doc_dict).insert()
				attendance.submit()
			except (DuplicateAttendanceError, OverlappingShiftAttendanceError, Exception):
				if not artech_engine.flags.in_test:
					artech_engine.db.rollback(save_point=savepoint)
				continue
		if not artech_engine.flags.in_test:
			artech_engine.db.commit()  # nosemgrep


@artech_engine.whitelist()
def get_unmarked_days(
	employee: str, from_date: str | date, to_date: str | date, exclude_holidays: str | int = 0
) -> list:
	joining_date, relieving_date = artech_engine.get_cached_value(
		"Employee", employee, ["date_of_joining", "relieving_date"]
	)

	from_date = max(getdate(from_date), joining_date or getdate(from_date))
	to_date = min(getdate(to_date), relieving_date or getdate(to_date))

	records = artech_engine.get_all(
		"Attendance",
		fields=["attendance_date", "employee"],
		filters=[
			["attendance_date", ">=", from_date],
			["attendance_date", "<=", to_date],
			["employee", "=", employee],
			["docstatus", "!=", 2],
		],
	)

	marked_days = [getdate(record.attendance_date) for record in records]

	if cint(exclude_holidays):
		holiday_dates = get_holiday_dates_between_range(
			employee, from_date, to_date, raise_exception_for_holiday_list=False
		)
		holidays = [getdate(record) for record in holiday_dates]
		marked_days.extend(holidays)

	unmarked_days = []

	while from_date <= to_date:
		if from_date not in marked_days:
			unmarked_days.append(from_date)

		from_date = add_days(from_date, 1)

	return unmarked_days
