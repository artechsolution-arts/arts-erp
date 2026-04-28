# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


from artech_engine.model.document import Document


class TargetDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		distribution_id: DF.Link
		fiscal_year: DF.Link
		item_group: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		target_amount: DF.Float
		target_qty: DF.Float
	# end: auto-generated types

	pass
