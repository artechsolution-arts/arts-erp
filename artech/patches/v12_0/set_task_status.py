import artech_engine


def execute():
	artech_engine.reload_doctype("Task")

	# add "Completed" if customized
	property_setter_name = artech_engine.db.exists(
		"Property Setter", dict(doc_type="Task", field_name="status", property="options")
	)
	if property_setter_name:
		property_setter = artech_engine.get_doc("Property Setter", property_setter_name)
		if "Completed" not in property_setter.value:
			property_setter.value = property_setter.value + "\nCompleted"
			property_setter.save()

	# renamed default status to Completed as status "Closed" is ambiguous
	artech_engine.db.sql('update tabTask set status = "Completed" where status = "Closed"')
