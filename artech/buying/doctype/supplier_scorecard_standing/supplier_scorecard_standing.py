# Copyright (c) 2017, Artech and contributors
# For license information, please see license.txt


import artech_engine
from artech_engine.model.document import Document


class SupplierScorecardStanding(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		employee_link: DF.Link | None
		max_grade: DF.Percent
		min_grade: DF.Percent
		notify_employee: DF.Check
		notify_supplier: DF.Check
		prevent_pos: DF.Check
		prevent_rfqs: DF.Check
		standing_color: DF.Literal["Blue", "Purple", "Green", "Yellow", "Orange", "Red"]
		standing_name: DF.Data | None
		warn_pos: DF.Check
		warn_rfqs: DF.Check
	# end: auto-generated types

	pass


@artech_engine.whitelist()
def get_scoring_standing(standing_name: str):
	standing = artech_engine.get_doc("Supplier Scorecard Standing", standing_name)

	return standing


@artech_engine.whitelist()
def get_standings_list():
	standings = artech_engine.db.sql(
		"""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Standing` scs""",
		{},
		as_dict=1,
	)

	return standings
