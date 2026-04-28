# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


from artech_engine.model.document import Document


class ActivityType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		activity_type: DF.Data
		billing_rate: DF.Currency
		costing_rate: DF.Currency
		disabled: DF.Check
	# end: auto-generated types

	pass
