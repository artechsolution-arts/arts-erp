# Copyright (c) 2015, Artech and Contributors


import json

import artech_engine
from artech_engine import _, throw
from artech_engine.desk.form.assign_to import clear, close_all_assignments
from artech_engine.model.mapper import get_mapped_doc
from artech_engine.query_builder.functions import Max, Min, Sum
from artech_engine.utils import add_days, add_to_date, cstr, date_diff, flt, get_link_to_form, getdate, today
from artech_engine.utils.data import format_date
from artech_engine.utils.nestedset import NestedSet


class CircularReferenceError(artech_engine.ValidationError):
	pass


class ParentIsGroupError(artech_engine.ValidationError):
	pass


class Task(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.projects.doctype.task_depends_on.task_depends_on import TaskDependsOn

		act_end_date: DF.Date | None
		act_start_date: DF.Date | None
		actual_time: DF.Float
		closing_date: DF.Date | None
		color: DF.Color | None
		company: DF.Link | None
		completed_by: DF.Link | None
		completed_on: DF.Date | None
		department: DF.Link | None
		depends_on: DF.Table[TaskDependsOn]
		depends_on_tasks: DF.Code | None
		description: DF.TextEditor | None
		duration: DF.Int
		exp_end_date: DF.Datetime | None
		exp_start_date: DF.Datetime | None
		expected_time: DF.Float
		is_group: DF.Check
		is_milestone: DF.Check
		is_template: DF.Check
		issue: DF.Link | None
		lft: DF.Int
		old_parent: DF.Data | None
		parent_task: DF.Link | None
		priority: DF.Literal["Low", "Medium", "High", "Urgent"]
		progress: DF.Percent
		project: DF.Link | None
		review_date: DF.Date | None
		rgt: DF.Int
		start: DF.Int
		status: DF.Literal[
			"Open", "Working", "Pending Review", "Overdue", "Template", "Completed", "Cancelled"
		]
		subject: DF.Data
		task_weight: DF.Float
		template_task: DF.Data | None
		total_billing_amount: DF.Currency
		total_costing_amount: DF.Currency
		type: DF.Link | None
	# end: auto-generated types

	nsm_parent_field = "parent_task"

	def get_customer_details(self):
		cust = artech_engine.db.sql("select customer_name from `tabCustomer` where name=%s", self.customer)
		if cust:
			ret = {"customer_name": cust and cust[0][0] or ""}
			return ret

	def validate(self):
		self.validate_dates()
		self.validate_progress()
		self.validate_status()
		self.update_depends_on()
		self.validate_dependencies_for_template_task()
		self.validate_completed_on()
		self.set_default_end_date_if_missing()
		self.validate_parent_is_group()

	def validate_dates(self):
		self.validate_from_to_dates("exp_start_date", "exp_end_date")
		self.validate_from_to_dates("act_start_date", "act_end_date")
		self.validate_parent_expected_end_date()
		self.validate_parent_project_dates()

	def set_default_end_date_if_missing(self):
		if self.exp_start_date and self.expected_time and not self.exp_end_date:
			self.exp_end_date = add_to_date(self.exp_start_date, hours=self.expected_time)

	def validate_parent_expected_end_date(self):
		if not self.parent_task or not self.exp_end_date:
			return

		parent_exp_end_date = artech_engine.db.get_value("Task", self.parent_task, "exp_end_date")
		if not parent_exp_end_date:
			return

		if getdate(self.exp_end_date) > getdate(parent_exp_end_date):
			artech_engine.throw(
				_(
					"Expected End Date should be less than or equal to parent task's Expected End Date {0}."
				).format(format_date(parent_exp_end_date)),
				artech_engine.exceptions.InvalidDates,
			)

	def validate_parent_project_dates(self):
		if not self.project or artech_engine.in_test:
			return

		if project_end_date := artech_engine.db.get_value("Project", self.project, "expected_end_date"):
			project_end_date = getdate(project_end_date)
			for fieldname in ("exp_start_date", "exp_end_date", "act_start_date", "act_end_date"):
				task_date = self.get(fieldname)
				if task_date and date_diff(project_end_date, getdate(task_date)) < 0:
					artech_engine.throw(
						_("{0}'s {1} cannot be after {2}'s Expected End Date.").format(
							artech_engine.bold(artech_engine.get_desk_link("Task", self.name)),
							_(self.meta.get_label(fieldname)),
							artech_engine.bold(artech_engine.get_desk_link("Project", self.project)),
						),
						artech_engine.exceptions.InvalidDates,
					)

	def validate_status(self):
		if self.is_template and self.status != "Template":
			self.status = "Template"
		if self.status == "Template" and not self.is_template:
			self.status = "Open"
		if self.status != self.get_db_value("status") and self.status == "Completed":
			for d in self.depends_on:
				if artech_engine.db.get_value("Task", d.task, "status") not in ("Completed", "Cancelled"):
					artech_engine.throw(
						_(
							"Cannot complete task {0} as its dependant task {1} are not completed / cancelled."
						).format(artech_engine.bold(self.name), artech_engine.bold(d.task))
					)

			close_all_assignments(self.doctype, self.name)

	def validate_progress(self):
		if flt(self.progress or 0) > 100:
			artech_engine.throw(_("Progress % for a task cannot be more than 100."))

		if self.status == "Completed":
			self.progress = 100

	def validate_dependencies_for_template_task(self):
		if self.is_template:
			self.validate_parent_template_task()
			self.validate_depends_on_tasks()

	def validate_parent_template_task(self):
		if self.parent_task:
			if not artech_engine.db.get_value("Task", self.parent_task, "is_template"):
				artech_engine.throw(
					_("Parent Task {0} is not a Template Task").format(
						get_link_to_form("Task", self.parent_task)
					)
				)

	def validate_depends_on_tasks(self):
		if self.depends_on:
			for task in self.depends_on:
				if not artech_engine.db.get_value("Task", task.task, "is_template"):
					artech_engine.throw(
						_("Dependent Task {0} is not a Template Task").format(
							get_link_to_form("Task", task.task)
						)
					)

	def validate_completed_on(self):
		if self.completed_on and getdate(self.completed_on) > getdate():
			artech_engine.throw(_("Completed On cannot be greater than Today"))

	def validate_parent_is_group(self):
		if self.parent_task:
			if not artech_engine.db.get_value("Task", self.parent_task, "is_group"):
				artech_engine.throw(
					_("Parent Task {0} must be a Group Task").format(
						get_link_to_form("Task", self.parent_task)
					),
					ParentIsGroupError,
				)

	def update_depends_on(self):
		depends_on_tasks = ""
		for d in self.depends_on:
			if d.task and d.task not in depends_on_tasks:
				depends_on_tasks += d.task + ","
		self.depends_on_tasks = depends_on_tasks

	def update_nsm_model(self):
		artech_engine.utils.nestedset.update_nsm(self)

	def on_update(self):
		self.update_nsm_model()
		self.check_recursion()
		self.reschedule_dependent_tasks()
		self.update_project()
		self.unassign_todo()
		self.populate_depends_on()

	def unassign_todo(self):
		if self.status == "Completed":
			close_all_assignments(self.doctype, self.name)
		if self.status == "Cancelled":
			clear(self.doctype, self.name)

	def update_time_and_costing(self):
		TimesheetDetail = artech_engine.qb.DocType("Timesheet Detail")
		tl = (
			artech_engine.qb.from_(TimesheetDetail)
			.select(
				Min(TimesheetDetail.from_time).as_("start_date"),
				Max(TimesheetDetail.to_time).as_("end_date"),
				Sum(TimesheetDetail.billing_amount).as_("total_billing_amount"),
				Sum(TimesheetDetail.costing_amount).as_("total_costing_amount"),
				Sum(TimesheetDetail.hours).as_("time"),
				Sum(TimesheetDetail.base_costing_amount).as_("base_costing_amount"),
				Sum(TimesheetDetail.base_billing_amount).as_("base_billing_amount"),
			)
			.where((TimesheetDetail.task == self.name) & (TimesheetDetail.docstatus == 1))
		).run(as_dict=True)[0]
		self.total_costing_amount = tl.base_costing_amount
		self.total_billing_amount = tl.base_billing_amount
		self.actual_time = tl.time
		self.act_start_date = tl.start_date
		self.act_end_date = tl.end_date

	def update_project(self):
		if self.project and not self.flags.from_project:
			artech_engine.get_cached_doc("Project", self.project).update_project()

	def check_recursion(self):
		if self.flags.ignore_recursion_check:
			return
		check_list = [["task", "parent"], ["parent", "task"]]
		for d in check_list:
			task_list, count = [self.name], 0
			while len(task_list) > count:
				tasks = artech_engine.db.sql(
					" select {} from `tabTask Depends On` where {} = {} ".format(d[0], d[1], "%s"),
					cstr(task_list[count]),
				)
				count = count + 1
				for b in tasks:
					if b[0] == self.name:
						artech_engine.throw(_("Circular Reference Error"), CircularReferenceError)
					if b[0]:
						task_list.append(b[0])

				if count == 15:
					break

	def reschedule_dependent_tasks(self):
		end_date = self.exp_end_date or self.act_end_date
		if end_date:
			for task_name in artech_engine.db.sql(
				"""
				select name from `tabTask` as parent
				where parent.project = %(project)s
					and parent.name in (
						select parent from `tabTask Depends On` as child
						where child.task = %(task)s and child.project = %(project)s)
			""",
				{"project": self.project, "task": self.name},
				as_dict=1,
			):
				task = artech_engine.get_doc("Task", task_name.name)
				if (
					task.exp_start_date
					and task.exp_end_date
					and task.exp_start_date < end_date
					and task.status == "Open"
				):
					task_duration = date_diff(task.exp_end_date, task.exp_start_date)
					task.exp_start_date = add_days(end_date, 1)
					task.exp_end_date = add_days(task.exp_start_date, task_duration)
					task.flags.ignore_recursion_check = True
					task.save()

	def has_webform_permission(self):
		project_user = artech_engine.db.get_value(
			"Project User", {"parent": self.project, "user": artech_engine.session.user}, "user"
		)
		if project_user:
			return True

	def populate_depends_on(self):
		if self.parent_task:
			parent = artech_engine.get_doc("Task", self.parent_task)
			if self.name not in [row.task for row in parent.depends_on]:
				parent.append(
					"depends_on", {"doctype": "Task Depends On", "task": self.name, "subject": self.subject}
				)
				parent.save()

	def on_trash(self):
		if check_if_child_exists(self.name):
			throw(_("Child Task exists for this Task. You can not delete this Task."))

		self.update_nsm_model()

	def after_delete(self):
		self.update_project()

	def update_status(self):
		if self.status not in ("Cancelled", "Completed") and self.exp_end_date:
			from datetime import datetime

			if self.exp_end_date < datetime.now():
				self.db_set("status", "Overdue", update_modified=False)
				self.update_project()


@artech_engine.whitelist()
def check_if_child_exists(name: str):
	child_tasks = artech_engine.get_all("Task", filters={"parent_task": name})
	child_tasks = [get_link_to_form("Task", task.name) for task in child_tasks]
	return child_tasks


@artech_engine.whitelist()
@artech_engine.validate_and_sanitize_search_inputs
def get_project(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict):
	from artech.controllers.queries import get_match_cond

	meta = artech_engine.get_meta(doctype)
	searchfields = meta.get_search_fields()
	search_columns = ", " + ", ".join(searchfields) if searchfields else ""
	search_cond = " or " + " or ".join(field + " like %(txt)s" for field in searchfields)

	return artech_engine.db.sql(
		f""" select name {search_columns} from `tabProject`
		where %(key)s like %(txt)s
			%(mcond)s
			{search_cond}
		order by name
		limit %(page_len)s offset %(start)s""",
		{
			"key": searchfield,
			"txt": "%" + txt + "%",
			"mcond": get_match_cond(doctype),
			"start": start,
			"page_len": page_len,
		},
	)


@artech_engine.whitelist()
def set_multiple_status(names: str, status: str):
	names = json.loads(names)
	for name in names:
		task = artech_engine.get_doc("Task", name)
		task.status = status
		task.save()


def set_tasks_as_overdue():
	tasks = artech_engine.get_all(
		"Task",
		filters={"status": ["not in", ["Cancelled", "Completed"]]},
		fields=["name", "status", "review_date"],
	)
	for task in tasks:
		if task.status == "Pending Review":
			if getdate(task.review_date) > getdate(today()):
				continue
		artech_engine.get_doc("Task", task.name).update_status()


@artech_engine.whitelist()
def make_timesheet(source_name: str, target_doc: dict | None = None, ignore_permissions: bool = False):
	def set_missing_values(source: dict, target: dict) -> None:
		target.parent_project = source.project
		target.append(
			"time_logs",
			{
				"hours": source.actual_time,
				"completed": source.status == "Completed",
				"project": source.project,
				"task": source.name,
			},
		)

	doclist = get_mapped_doc(
		"Task",
		source_name,
		{"Task": {"doctype": "Timesheet"}},
		target_doc,
		postprocess=set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	return doclist


@artech_engine.whitelist()
def get_children(
	doctype: str,
	parent: str | None = None,
	task: str | None = None,
	project: str | None = None,
	is_root: bool = False,
):
	filters = [["docstatus", "<", "2"]]

	if task:
		filters.append(["parent_task", "=", task])
	elif parent and not is_root:
		# via expand child
		filters.append(["parent_task", "=", parent])
	else:
		from artech_engine.query_builder import Field, functions

		filters.append(functions.IfNull(Field("parent_task"), "") == "")

	if project:
		filters.append(["project", "=", project])

	tasks = artech_engine.get_list(
		doctype,
		fields=["name as value", "subject as title", "is_group as expandable"],
		filters=filters,
		order_by="name",
	)

	# return tasks
	return tasks


@artech_engine.whitelist()
def add_node():
	from artech_engine.desk.treeview import make_tree_args

	args = artech_engine.form_dict
	args.update({"name_field": "subject"})
	args = make_tree_args(**args)

	if args.parent_task == "All Tasks" or args.parent_task == args.project:
		args.parent_task = None

	artech_engine.get_doc(args).insert()


@artech_engine.whitelist()
def add_multiple_tasks(data: str, parent: str):
	data = json.loads(data)
	new_doc = {"doctype": "Task", "parent_task": parent if parent != "All Tasks" else ""}
	new_doc["project"] = artech_engine.db.get_value("Task", {"name": parent}, "project") or ""

	for d in data:
		if not d.get("subject"):
			continue
		new_doc["subject"] = d.get("subject")
		new_task = artech_engine.get_doc(new_doc)
		new_task.insert()


def on_doctype_update():
	artech_engine.db.add_index("Task", ["lft", "rgt"])
