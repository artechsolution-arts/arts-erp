import artech_engine
from artech_engine.query_builder import DocType


def execute():
	Asset = DocType("Asset")

	query = (
		artech_engine.qb.update(Asset)
		.set(Asset.status, "Draft")
		.where((Asset.docstatus == 0) & ((Asset.status.isnull()) | (Asset.status == "")))
	)
	query.run()
