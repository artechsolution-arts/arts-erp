import artech_engine
from artech_engine.utils import cint


def execute():
	"""Get 'Disable CWIP Accounting value' from Asset Settings, set it in 'Enable Capital Work in Progress Accounting' field
	in Company, delete Asset Settings"""

	if artech_engine.db.exists("DocType", "Asset Settings"):
		artech_engine.reload_doctype("Asset Category")
		cwip_value = artech_engine.db.get_single_value("Asset Settings", "disable_cwip_accounting")

		artech_engine.db.sql("""UPDATE `tabAsset Category` SET enable_cwip_accounting = %s""", cint(cwip_value))

		artech_engine.db.sql("""DELETE FROM `tabSingles` where doctype = 'Asset Settings'""")
		artech_engine.delete_doc_if_exists("DocType", "Asset Settings")
