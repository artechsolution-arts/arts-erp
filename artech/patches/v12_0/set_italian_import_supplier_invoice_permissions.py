import artech_engine

from artech.regional.italy.setup import add_permissions


def execute():
	countries = artech_engine.get_all("Company", fields="country")
	countries = [country["country"] for country in countries]
	if "Italy" in countries:
		add_permissions()
