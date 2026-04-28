# Copyright (c) 2019, Artech and contributors
# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import get_link_to_form


class ProjectTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.projects.doctype.project_template_task.project_template_task import (
			ProjectTemplateTask,
		)

		disabled: DF.Check
		project_type: DF.Link | None
		tasks: DF.Table[ProjectTemplateTask]
	# end: auto-generated types

	def validate(self):
		self.validate_dependencies()

	def validate_dependencies(self):
		for task in self.tasks:
			task_details = artech_engine.get_doc("Task", task.task)
			if task_details.depends_on:
				for dependency_task in task_details.depends_on:
					if not self.check_dependent_task_presence(dependency_task.task):
						task_details_format = get_link_to_form("Task", task_details.name)
						dependency_task_format = get_link_to_form("Task", dependency_task.task)
						artech_engine.throw(
							_("Task {0} depends on Task {1}. Please add Task {1} to the Tasks list.").format(
								artech_engine.bold(task_details_format), artech_engine.bold(dependency_task_format)
							)
						)

	def check_dependent_task_presence(self, task):
		for task_details in self.tasks:
			if task_details.task == task:
				return True
		return False
