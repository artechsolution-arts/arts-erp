import artech_engine
from artech_engine.query_builder import DocType


def execute():
	qlr = DocType("Quotation Lost Reason Detail")
	quotation = DocType("Quotation")

	sub_query = artech_engine.qb.from_(quotation).select(quotation.name)
	query = artech_engine.qb.from_(qlr).delete().where(qlr.parent.notin(sub_query))
	query.run()
