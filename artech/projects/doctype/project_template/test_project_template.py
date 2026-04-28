# Copyright (c) 2019, Artech and Contributors
# See license.txt

import artech_engine

from artech.projects.doctype.task.test_task import create_task
from artech.tests.utils import ArtechTestSuite


class TestProjectTemplate(ArtechTestSuite):
	pass


def make_project_template(project_template_name, project_tasks=None):
	if project_tasks is None:
		project_tasks = []
	if not artech_engine.db.exists("Project Template", project_template_name):
		project_tasks = project_tasks or [
			create_task(subject="_Test Template Task 1", is_template=1, begin=0, duration=3),
			create_task(subject="_Test Template Task 2", is_template=1, begin=0, duration=2),
		]
		doc = artech_engine.get_doc(doctype="Project Template", name=project_template_name)
		for task in project_tasks:
			doc.append("tasks", {"task": task.name})
		doc.insert()

	return artech_engine.get_doc("Project Template", project_template_name)
