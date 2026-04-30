# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import get_link_to_form


class DepartmentApprover(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		approver: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass


@artech_engine.whitelist()
@artech_engine.validate_and_sanitize_search_inputs
def get_approvers(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict):
	if not filters.get("employee"):
		artech_engine.throw(_("Please select Employee first."))

	approvers = []
	department_details = {}
	department_list = []
	employee = artech_engine.get_value(
		"Employee",
		filters.get("employee"),
		["employee_name", "department", "leave_approver", "expense_approver", "shift_request_approver"],
		as_dict=True,
	)

	employee_department = filters.get("department") or employee.department
	if employee_department:
		department_details = artech_engine.db.get_value(
			"Department", {"name": employee_department}, ["lft", "rgt"], as_dict=True
		)
	if department_details:
		department_list = artech_engine.db.sql(
			"""select name from `tabDepartment` where lft <= %s
			and rgt >= %s
			and disabled=0
			order by lft desc""",
			(department_details.lft, department_details.rgt),
			as_list=True,
		)

	if filters.get("doctype") == "Leave Application" and employee.leave_approver:
		approvers.append(
			artech_engine.db.get_value("User", employee.leave_approver, ["name", "first_name", "last_name"])
		)

	if filters.get("doctype") == "Expense Claim" and employee.expense_approver:
		approvers.append(
			artech_engine.db.get_value("User", employee.expense_approver, ["name", "first_name", "last_name"])
		)

	if filters.get("doctype") == "Shift Request" and employee.shift_request_approver:
		approvers.append(
			artech_engine.db.get_value("User", employee.shift_request_approver, ["name", "first_name", "last_name"])
		)

	if filters.get("doctype") == "Leave Application":
		parentfield = "leave_approvers"
		field_name = "Leave Approver"
	elif filters.get("doctype") == "Expense Claim":
		parentfield = "expense_approvers"
		field_name = "Expense Approver"
	elif filters.get("doctype") == "Shift Request":
		parentfield = "shift_request_approver"
		field_name = "Shift Request Approver"
	if department_list:
		for d in department_list:
			approvers += artech_engine.db.sql(
				"""select user.name, user.first_name, user.last_name from
				tabUser user, `tabDepartment Approver` approver where
				approver.parent = %s
				and user.name like %s
				and approver.parentfield = %s
				and approver.approver=user.name""",
				(d, "%" + txt + "%", parentfield),
				as_list=True,
			)

	if len(approvers) == 0:
		error_msg = _("Please set {0} for the Employee: {1}").format(
			artech_engine.bold(_(field_name)),
			get_link_to_form("Employee", filters.get("employee"), employee.employee_name),
		)
		if department_list:
			error_msg += " " + _("or for the Employee's Department: {0}").format(
				get_link_to_form("Department", employee_department)
			)
		artech_engine.throw(error_msg, title=_("{0} Missing").format(_(field_name)))

	return set(tuple(approver) for approver in approvers)
