import click

import artech_engine


def execute():
	frappe_v = artech_engine.get_attr("artech_engine" + ".__version__")
	hrms_v = artech_engine.get_attr("artech_hrms" + ".__version__")

	WIKI_URL = "https://github.com/artech_engine/artech_hrms/wiki/Changes-to-branching-and-versioning"

	if frappe_v.startswith("14") and hrms_v.startswith("15"):
		message = f"""
			The `develop` branch of Frappe HR is no longer compatible with Frappe & ERPNext's `version-14`.
			Since you are using ERPNext/Frappe `version-14` please switch Frappe HR's branch to `version-14` and then proceed with the update.\n\t
			You can switch the branch by following the steps mentioned here: {WIKI_URL}
		"""
		click.secho(message, fg="red")

		artech_engine.throw(message)  # nosemgrep
