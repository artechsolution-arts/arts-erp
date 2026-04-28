import artech_engine


def execute():
	"""
	- Don't use batchwise valuation for existing batches.
	- Only batches created after this patch shoule use it.
	"""

	batch = artech_engine.qb.DocType("Batch")
	artech_engine.qb.update(batch).set(batch.use_batchwise_valuation, 0).run()
