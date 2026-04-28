import artech_engine


def execute():
	artech_engine.reload_doc("setup", "doctype", "Email Digest")
	artech_engine.reload_doc("setup", "doctype", "Email Digest Recipient")
	email_digests = artech_engine.db.get_list("Email Digest", fields=["name", "recipient_list"])
	for email_digest in email_digests:
		if email_digest.recipient_list:
			for recipient in email_digest.recipient_list.split("\n"):
				doc = artech_engine.get_doc(
					{
						"doctype": "Email Digest Recipient",
						"parenttype": "Email Digest",
						"parentfield": "recipients",
						"parent": email_digest.name,
						"recipient": recipient,
					}
				)
				doc.insert()
