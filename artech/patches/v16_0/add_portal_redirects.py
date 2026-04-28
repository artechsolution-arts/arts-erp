import artech_engine


def execute():
	if artech_engine.db.exists("Portal Menu Item", {"route": "/addresses", "reference_doctype": "Address"}) and (
		doc := artech_engine.get_doc("Portal Menu Item", {"route": "/addresses", "reference_doctype": "Address"})
	):
		doc.role = "Customer"
		doc.save()

	website_settings = artech_engine.get_single("Website Settings")
	website_settings.append("route_redirects", {"source": "addresses", "target": "address/list"})
	website_settings.append("route_redirects", {"source": "projects", "target": "project"})
	website_settings.save()
