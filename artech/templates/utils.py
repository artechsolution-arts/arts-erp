# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine
from artech_engine.utils import escape_html


@artech_engine.whitelist(allow_guest=True)
def send_message(sender: str, message: str, subject: str = "Website Query"):
	from artech_engine.www.contact import send_message as website_send_message

	website_send_message(sender, message, subject)

	message = escape_html(message)

	lead = customer = None
	customer = artech_engine.db.sql(
		"""select distinct dl.link_name from `tabDynamic Link` dl
		left join `tabContact` c on dl.parent=c.name where dl.link_doctype='Customer'
		and c.email_id = %s""",
		sender,
	)

	if not customer:
		lead = artech_engine.db.get_value("Lead", dict(email_id=sender))
		if not lead:
			new_lead = artech_engine.get_doc(
				doctype="Lead", email_id=sender, lead_name=sender.split("@")[0].title()
			).insert(ignore_permissions=True)

	opportunity = artech_engine.get_doc(
		doctype="Opportunity",
		opportunity_from="Customer" if customer else "Lead",
		status="Open",
		title=subject,
		contact_email=sender,
	)

	if customer:
		opportunity.party_name = customer[0][0]
	elif lead:
		opportunity.party_name = lead
	else:
		opportunity.party_name = new_lead.name

	opportunity.insert(ignore_permissions=True)

	comm = artech_engine.get_doc(
		{
			"doctype": "Communication",
			"subject": subject,
			"content": message,
			"sender": sender,
			"sent_or_received": "Received",
			"reference_doctype": "Opportunity",
			"reference_name": opportunity.name,
		}
	)
	comm.insert(ignore_permissions=True)
