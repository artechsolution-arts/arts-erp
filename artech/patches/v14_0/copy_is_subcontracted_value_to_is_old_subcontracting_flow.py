# Copyright (c) 2022, Artech and contributors
# For license information, please see license.txt

import artech_engine


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
		tab = artech_engine.qb.DocType(doctype).as_("tab")
		artech_engine.qb.update(tab).set(tab.is_old_subcontracting_flow, 1).where(tab.is_subcontracted == 1).run()
