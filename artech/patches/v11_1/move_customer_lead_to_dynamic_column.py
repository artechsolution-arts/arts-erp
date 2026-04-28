# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doctype("Quotation")
	artech_engine.db.sql(""" UPDATE `tabQuotation` set party_name = lead WHERE quotation_to = 'Lead' """)
	artech_engine.db.sql(""" UPDATE `tabQuotation` set party_name = customer WHERE quotation_to = 'Customer' """)

	artech_engine.reload_doctype("Opportunity")
	artech_engine.db.sql(""" UPDATE `tabOpportunity` set party_name = lead WHERE opportunity_from = 'Lead' """)
	artech_engine.db.sql(
		""" UPDATE `tabOpportunity` set party_name = customer WHERE opportunity_from = 'Customer' """
	)
