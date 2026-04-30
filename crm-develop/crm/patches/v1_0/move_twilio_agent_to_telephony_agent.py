import artech_engine


def execute():
	if not artech_engine.db.exists("DocType", "CRM Telephony Agent"):
		artech_engine.reload_doctype("CRM Telephony Agent", force=True)

	if artech_engine.db.exists("DocType", "Twilio Agents") and artech_engine.db.count("Twilio Agents") == 0:
		return

	agents = artech_engine.db.sql("SELECT * FROM `tabTwilio Agents`", as_dict=True)
	if agents:
		for agent in agents:
			doc = artech_engine.get_doc(
				{
					"doctype": "CRM Telephony Agent",
					"creation": agent.get("creation"),
					"modified": agent.get("modified"),
					"modified_by": agent.get("modified_by"),
					"owner": agent.get("owner"),
					"user": agent.get("user"),
					"twilio_number": agent.get("twilio_number"),
					"user_name": agent.get("user_name"),
					"twilio": True,
				}
			)
			doc.db_insert()
