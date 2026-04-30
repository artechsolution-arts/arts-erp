# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import getdate

from hrms.hr.utils import update_employee_work_history, validate_active_employee


class EmployeePromotion(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from hrms.hr.doctype.employee_property_history.employee_property_history import (
			EmployeePropertyHistory,
		)

		amended_from: DF.Link | None
		company: DF.Link | None
		current_ctc: DF.Currency
		department: DF.Link | None
		employee: DF.Link
		employee_name: DF.Data | None
		promotion_date: DF.Date
		promotion_details: DF.Table[EmployeePropertyHistory]
		revised_ctc: DF.Currency
		salary_currency: DF.Link | None
	# end: auto-generated types

	def validate(self):
		validate_active_employee(self.employee)

	def before_submit(self):
		if getdate(self.promotion_date) > getdate():
			artech_engine.throw(
				_("Employee Promotion cannot be submitted before Promotion Date"),
				artech_engine.DocstatusTransitionError,
			)

	def on_submit(self):
		employee = artech_engine.get_doc("Employee", self.employee)
		employee = update_employee_work_history(employee, self.promotion_details, date=self.promotion_date)

		if self.revised_ctc:
			employee.ctc = self.revised_ctc

		employee.save()

	def on_cancel(self):
		employee = artech_engine.get_doc("Employee", self.employee)
		employee = update_employee_work_history(employee, self.promotion_details, cancel=True)

		if self.revised_ctc:
			employee.ctc = self.current_ctc

		employee.save()
