# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("projects", "doctype", "project_template")
	artech_engine.reload_doc("projects", "doctype", "project_template_task")
	artech_engine.reload_doc("projects", "doctype", "task")

	# Update property setter status if any
	property_setter = artech_engine.db.get_value(
		"Property Setter", {"doc_type": "Task", "field_name": "status", "property": "options"}
	)

	if property_setter:
		property_setter_doc = artech_engine.get_doc(
			"Property Setter", {"doc_type": "Task", "field_name": "status", "property": "options"}
		)
		property_setter_doc.value += "\nTemplate"
		property_setter_doc.save()

	for template_name in artech_engine.get_all("Project Template"):
		template = artech_engine.get_doc("Project Template", template_name.name)
		replace_tasks = False
		new_tasks = []
		for task in template.tasks:
			if task.subject:
				replace_tasks = True
				new_task = artech_engine.get_doc(
					doctype="Task",
					subject=task.subject,
					start=task.start,
					duration=task.duration,
					task_weight=task.task_weight,
					description=task.description,
					is_template=1,
				).insert()
				new_tasks.append(new_task)

		if replace_tasks:
			template.tasks = []
			for tsk in new_tasks:
				template.append("tasks", {"task": tsk.name, "subject": tsk.subject})
			template.save()
