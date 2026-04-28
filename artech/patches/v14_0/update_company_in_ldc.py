# Copyright (c) 2023, Artech and Contributors
# License: MIT. See LICENSE


import artech_engine

from artech import get_default_company


def execute():
	company = get_default_company()
	if company:
		for d in artech_engine.get_all("Lower Deduction Certificate", pluck="name"):
			artech_engine.db.set_value("Lower Deduction Certificate", d, "company", company, update_modified=False)
