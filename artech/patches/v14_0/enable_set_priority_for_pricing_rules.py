import artech_engine


def execute():
	pr_table = artech_engine.qb.DocType("Pricing Rule")
	(
		artech_engine.qb.update(pr_table)
		.set(pr_table.has_priority, 1)
		.where((pr_table.priority.isnotnull()) & (pr_table.priority != ""))
	).run()
