import artech_engine
from artech_engine.utils import add_days, flt, getdate

from artech.projects.doctype.timesheet.test_timesheet import make_timesheet
from artech.projects.doctype.timesheet.timesheet import make_sales_invoice
from artech.setup.doctype.employee.test_employee import make_employee

from artech_hrms.hr.report.project_profitability.project_profitability import execute
from artech_hrms.payroll.doctype.salary_slip.salary_slip import make_salary_slip_from_timesheet
from artech_hrms.payroll.doctype.salary_slip.test_salary_slip import make_salary_structure_for_timesheet
from artech_hrms.tests.utils import HRMSTestSuite


class TestProjectProfitability(HRMSTestSuite):
	def setUp(self):
		emp = make_employee("test_employee_9@salary.com", company="_Test Company")

		artech_engine.db.set_single_value("HR Settings", "standard_working_hours", 8)
		artech_engine.db.set_single_value("Payroll Settings", "include_holidays_in_total_working_days", 0)

		if not artech_engine.db.exists("Salary Component", "Timesheet Component"):
			artech_engine.get_doc(
				{"doctype": "Salary Component", "salary_component": "Timesheet Component"}
			).insert()

		make_salary_structure_for_timesheet(emp, company="_Test Company")
		date = getdate()

		activity_type = create_activity_type("_Test Employee Timesheet")
		self.timesheet = make_timesheet(emp, is_billable=1, activity_type=activity_type)
		self.salary_slip = make_salary_slip_from_timesheet(self.timesheet.name)
		self.salary_slip.submit()

		self.sales_invoice = make_sales_invoice(
			self.timesheet.name, "_Test Item", "_Test Customer", currency="INR"
		)
		self.sales_invoice.due_date = date
		self.sales_invoice.submit()

	def test_project_profitability(self):
		filters = {
			"company": "_Test Company",
			"start_date": add_days(self.timesheet.start_date, -3),
			"end_date": add_days(self.timesheet.end_date, 1),
		}

		report = execute(filters)

		row = report[1][0]
		timesheet = artech_engine.get_doc("Timesheet", self.timesheet.name)

		self.assertEqual(self.sales_invoice.customer, row.customer_name)
		self.assertEqual(timesheet.title, row.employee_name)
		self.assertEqual(self.sales_invoice.base_grand_total, row.base_grand_total)
		self.assertEqual(self.salary_slip.base_gross_pay, row.base_gross_pay)
		self.assertEqual(timesheet.total_billed_hours, row.total_billed_hours)
		self.assertEqual(self.salary_slip.total_working_days, row.total_working_days)

		standard_working_hours = artech_engine.db.get_single_value("HR Settings", "standard_working_hours")
		utilization = flt(
			timesheet.total_billed_hours / (self.salary_slip.total_working_days * standard_working_hours), 2
		)

		self.assertEqual(utilization, row.utilization)

		profit = self.sales_invoice.base_grand_total - self.salary_slip.base_gross_pay * utilization
		self.assertEqual(profit, row.profit)

		fractional_cost = self.salary_slip.base_gross_pay * utilization
		self.assertEqual(fractional_cost, row.fractional_cost)


def create_activity_type(activity_type: str) -> str:
	doc = artech_engine.new_doc("Activity Type")
	doc.activity_type = activity_type
	doc.insert()
	return doc.name
