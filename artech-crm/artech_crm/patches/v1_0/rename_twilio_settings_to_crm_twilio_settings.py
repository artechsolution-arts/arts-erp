import artech_engine
from artech_engine.model.rename_doc import rename_doc


def execute():
	if artech_engine.db.exists("DocType", "Twilio Settings"):
		artech_engine.flags.ignore_route_conflict_validation = True
		rename_doc("DocType", "Twilio Settings", "CRM Twilio Settings")
		artech_engine.flags.ignore_route_conflict_validation = False

		artech_engine.reload_doctype("CRM Twilio Settings", force=True)

	if artech_engine.db.exists("__Auth", {"doctype": "Twilio Settings"}):
		Auth = artech_engine.qb.DocType("__Auth")
		result = artech_engine.qb.from_(Auth).select("*").where(Auth.doctype == "Twilio Settings").run(as_dict=True)

		for row in result:
			artech_engine.qb.into(Auth).insert(
				"CRM Twilio Settings", "CRM Twilio Settings", row.fieldname, row.password, row.encrypted
			).run()
