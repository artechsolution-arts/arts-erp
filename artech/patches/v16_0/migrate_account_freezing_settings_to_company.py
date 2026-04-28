import artech_engine


def execute():
	rows = artech_engine.db.sql(
		"""
		SELECT field, value
		FROM `tabSingles`
		WHERE doctype='Accounts Settings'
		AND field IN ('acc_frozen_upto', 'frozen_accounts_modifier')
		""",
		as_dict=True,
	)

	values = {row["field"]: row["value"] for row in rows}

	frozen_till = values.get("acc_frozen_upto")
	modifier = values.get("frozen_accounts_modifier")

	if not frozen_till and not modifier:
		return

	for company in artech_engine.get_all("Company", pluck="name"):
		artech_engine.db.set_value(
			"Company",
			company,
			{
				"accounts_frozen_till_date": frozen_till,
				"role_allowed_for_frozen_entries": modifier,
			},
		)
