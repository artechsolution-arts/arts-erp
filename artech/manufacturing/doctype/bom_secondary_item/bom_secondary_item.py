# Copyright (c) 2026, Artech and contributors
# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class BOMSecondaryItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		base_cost: DF.Currency
		conversion_factor: DF.Float
		cost: DF.Currency
		cost_allocation_per: DF.Percent
		description: DF.TextEditor | None
		image: DF.AttachImage | None
		is_legacy: DF.Check
		item_code: DF.Link
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		process_loss_per: DF.Percent
		process_loss_qty: DF.Float
		qty: DF.Float
		rate: DF.Currency
		stock_qty: DF.Float
		stock_uom: DF.Link | None
		type: DF.Literal["", "Co-Product", "By-Product", "Scrap", "Additional Finished Good"]
		uom: DF.Link
	# end: auto-generated types

	pass
