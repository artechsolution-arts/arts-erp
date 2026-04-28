import artech_engine


def execute():
	job_card = artech_engine.qb.DocType("Job Card")
	(
		artech_engine.qb.update(job_card)
		.set(job_card.status, "Completed")
		.where(
			(job_card.docstatus == 1)
			& (job_card.for_quantity <= job_card.total_completed_qty)
			& (job_card.status.isin(["Work In Progress", "Material Transferred"]))
		)
	).run()
