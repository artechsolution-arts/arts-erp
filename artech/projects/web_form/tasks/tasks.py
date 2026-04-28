import urllib.parse

import artech_engine


def get_context(context):
	if project := artech_engine.form_dict.project:
		title = artech_engine.utils.data.escape_html(project)
		route = "/projects?" + urllib.parse.urlencode({"project": project})
		context.parents = [{"title": title, "route": route}]
		context.success_url = route

	elif context.doc and (project := context.doc.get("project")):
		title = artech_engine.utils.data.escape_html(project)
		route = "/projects?" + urllib.parse.urlencode({"project": project})
		context.parents = [{"title": title, "route": route}]
		context.success_url = route
