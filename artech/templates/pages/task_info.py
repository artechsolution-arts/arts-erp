import artech_engine


def get_context(context):
	context.no_cache = 1

	task = artech_engine.get_doc("Task", artech_engine.form_dict.task)

	context.comments = artech_engine.get_all(
		"Communication",
		filters={"reference_name": task.name, "comment_type": "comment"},
		fields=["subject", "sender_full_name", "communication_date"],
	)

	context.doc = task
