import artech_engine


def execute():
	settings = artech_engine.db.get_singles_dict("Selling Settings", cast=True)

	artech_engine.reload_doc("crm", "doctype", "crm_settings")
	if settings:
		artech_engine.db.set_single_value(
			"CRM Settings",
			{
				"campaign_naming_by": settings.campaign_naming_by,
				"close_opportunity_after_days": settings.close_opportunity_after_days,
				"default_valid_till": settings.default_valid_till,
			},
		)
