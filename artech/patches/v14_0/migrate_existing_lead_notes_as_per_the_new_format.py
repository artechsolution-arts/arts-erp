import artech_engine
from artech_engine.utils import cstr, strip_html


def execute():
	for doctype in ("Lead", "Prospect", "Opportunity"):
		if not artech_engine.db.has_column(doctype, "notes"):
			continue

		dt = artech_engine.qb.DocType(doctype)
		records = (
			artech_engine.qb.from_(dt).select(dt.name, dt.notes).where(dt.notes.isnotnull() & dt.notes != "")
		).run(as_dict=True)

		for d in records:
			if strip_html(cstr(d.notes)).strip():
				doc = artech_engine.get_doc(doctype, d.name)
				doc.append("notes", {"note": d.notes})
				doc.update_child_table("notes")

		artech_engine.db.sql_ddl(f"alter table `tab{doctype}` drop column `notes`")
