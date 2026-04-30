import artech_engine


def execute():
	onboarding_template = artech_engine.qb.DocType("Employee Onboarding Template")
	(
		artech_engine.qb.update(onboarding_template)
		.set(onboarding_template.title, onboarding_template.designation)
		.where(onboarding_template.title.isnull())
	).run()

	separation_template = artech_engine.qb.DocType("Employee Separation Template")
	(
		artech_engine.qb.update(separation_template)
		.set(separation_template.title, separation_template.designation)
		.where(separation_template.title.isnull())
	).run()
