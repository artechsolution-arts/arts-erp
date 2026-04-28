import artech_engine


def execute():
	artech_engine.reload_doctype("Maintenance Visit")
	artech_engine.reload_doctype("Maintenance Visit Purpose")

	# Updates the Maintenance Schedule link to fetch serial nos
	from artech_engine.query_builder.functions import Coalesce

	mvp = artech_engine.qb.DocType("Maintenance Visit Purpose")
	mv = artech_engine.qb.DocType("Maintenance Visit")

	artech_engine.qb.update(mv).join(mvp).on(mvp.parent == mv.name).set(
		mv.maintenance_schedule, Coalesce(mvp.prevdoc_docname, "")
	).where((mv.maintenance_type == "Scheduled") & (mvp.prevdoc_docname.notnull()) & (mv.docstatus < 2)).run(
		as_dict=1
	)
