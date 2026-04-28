# Copyright (c) 2022, Artech and contributors
# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class ProspectOpportunity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amount: DF.Currency
		contact_person: DF.Link | None
		currency: DF.Link | None
		deal_owner: DF.Data | None
		expected_closing: DF.Date | None
		name: DF.Int | None
		opportunity: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		probability: DF.Percent
		stage: DF.Data | None
	# end: auto-generated types

	pass
