## temp utility

from contextlib import contextmanager

import artech_engine
from artech_engine import _
from artech_engine.utils import cstr

from artech.utilities.activation import get_level


def update_doctypes():
	for d in artech_engine.db.sql(
		"""select df.parent, df.fieldname
		from tabDocField df, tabDocType dt where df.fieldname
		like "%description%" and df.parent = dt.name and dt.istable = 1""",
		as_dict=1,
	):
		dt = artech_engine.get_doc("DocType", d.parent)

		for f in dt.fields:
			if f.fieldname == d.fieldname and f.fieldtype in ("Text", "Small Text"):
				f.fieldtype = "Text Editor"
				dt.save()
				break


def get_site_info(site_info):
	# called via hook
	company = artech_engine.db.get_single_value("Global Defaults", "default_company")
	domain = None

	if not company:
		company = artech_engine.db.sql("select name from `tabCompany` order by creation asc")
		company = company[0][0] if company else None

	if company:
		domain = artech_engine.get_cached_value("Company", cstr(company), "domain")

	return {"company": company, "domain": domain, "activation": get_level(site_info)}


@contextmanager
def payment_app_import_guard():
	marketplace_link = '<a href="https://artech_enginecloud.com/marketplace/apps/payments">Marketplace</a>'
	github_link = '<a href="https://github.com/artech_engine/payments/">GitHub</a>'
	msg = _("payments app is not installed. Please install it from {} or {}").format(
		marketplace_link, github_link
	)
	try:
		yield
	except ImportError:
		artech_engine.throw(msg, title=_("Missing Payments App"))
