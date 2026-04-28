import artech_engine
from artech_engine.query_builder import DocType


def execute():
	default_accounting_dimension()
	ADF = DocType("Accounting Dimension Filter")
	AD = DocType("Accounting Dimension")

	accounting_dimension_filter = (
		artech_engine.qb.from_(ADF)
		.join(AD)
		.on(AD.document_type == ADF.accounting_dimension)
		.select(ADF.name, AD.fieldname, ADF.accounting_dimension)
	).run(as_dict=True)

	for doc in accounting_dimension_filter:
		value = doc.fieldname or artech_engine.scrub(doc.accounting_dimension)
		artech_engine.db.set_value(
			"Accounting Dimension Filter",
			doc.name,
			"fieldname",
			value,
			update_modified=False,
		)


def default_accounting_dimension():
	ADF = DocType("Accounting Dimension Filter")
	for dim in ("Cost Center", "Project"):
		(
			artech_engine.qb.update(ADF)
			.set(ADF.fieldname, artech_engine.scrub(dim))
			.where(ADF.accounting_dimension == dim)
			.run()
		)
