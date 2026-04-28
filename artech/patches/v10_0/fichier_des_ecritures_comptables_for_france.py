# Copyright (c) 2018, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine

from artech.setup.doctype.company.company import install_country_fixtures


def execute():
	artech_engine.reload_doc("regional", "report", "fichier_des_ecritures_comptables_[fec]")
	for d in artech_engine.get_all("Company", filters={"country": "France"}):
		install_country_fixtures(d.name)
