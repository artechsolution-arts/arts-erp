# Copyright (c) 2023, Artech and Contributors
# License: MIT. See LICENSE


import artech_engine


def execute():
	navbar_settings = artech_engine.get_single("Navbar Settings")
	for item in navbar_settings.help_dropdown:
		if item.is_standard and item.route == "https://artech.com/docs/user/manual":
			item.route = "https://docs.artech.com/docs/v14/user/manual/en/introduction"

	navbar_settings.save()
