# For license information, please see license.txt


import artech_engine
from artech_engine import _

from artech import get_region


def check_deletion_permission(doc, method):
	region = get_region(doc.company)
	if region in ["Nepal"] and doc.docstatus != 0:
		artech_engine.throw(_("Deletion is not permitted for country {0}").format(region))
