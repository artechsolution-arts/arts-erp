import artech_engine


def get_context(context):
	context.no_cache = 1

	timelog = artech_engine.get_doc("Time Log", artech_engine.form_dict.timelog)

	context.doc = timelog
