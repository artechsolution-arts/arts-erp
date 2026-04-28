import artech_engine
from artech_engine.utils import cint


def execute():
	artech_engine.reload_doc("artech_integrations", "doctype", "woocommerce_settings")
	doc = artech_engine.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)
