import artech_engine
from pypika import Criterion


@artech_engine.whitelist()
def get_views(doctype: str):
	View = artech_engine.qb.DocType("CRM View Settings")
	query = (
		artech_engine.qb.from_(View)
		.select("*")
		.where(Criterion.any([View.user == "", View.user == artech_engine.session.user]))
	)
	if doctype:
		query = query.where(View.dt == doctype)
	views = query.run(as_dict=True)
	return views
