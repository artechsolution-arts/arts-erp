import artech_engine


def execute():
	artech_engine.reload_doctype("Opportunity")
	if artech_engine.db.has_column("Opportunity", "enquiry_from"):
		artech_engine.db.sql(
			""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''"""
		)

	if artech_engine.db.has_column("Opportunity", "lead") and artech_engine.db.has_column("Opportunity", "enquiry_from"):
		artech_engine.db.sql(
			""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''"""
		)

	if artech_engine.db.has_column("Opportunity", "customer") and artech_engine.db.has_column(
		"Opportunity", "enquiry_from"
	):
		artech_engine.db.sql(
			""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''"""
		)
