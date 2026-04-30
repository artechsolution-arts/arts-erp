import artech_engine
from artech_engine.model.rename_doc import rename_doc


def execute():
	if not artech_engine.db.exists("DocType", "FCRM Note"):
		artech_engine.flags.ignore_route_conflict_validation = True
		rename_doc("DocType", "CRM Note", "FCRM Note")
		artech_engine.flags.ignore_route_conflict_validation = False

		artech_engine.reload_doctype("FCRM Note", force=True)

	if artech_engine.db.exists("DocType", "FCRM Note") and artech_engine.db.count("FCRM Note") > 0:
		return

	notes = artech_engine.db.sql("SELECT * FROM `tabCRM Note`", as_dict=True)
	if notes:
		for note in notes:
			doc = artech_engine.get_doc(
				{
					"doctype": "FCRM Note",
					"creation": note.get("creation"),
					"modified": note.get("modified"),
					"modified_by": note.get("modified_by"),
					"owner": note.get("owner"),
					"title": note.get("title"),
					"content": note.get("content"),
					"reference_doctype": note.get("reference_doctype"),
					"reference_docname": note.get("reference_docname"),
				}
			)
			doc.db_insert()
