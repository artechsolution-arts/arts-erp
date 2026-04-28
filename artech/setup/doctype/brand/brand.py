# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine
from artech_engine.model.document import Document


class Brand(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.stock.doctype.item_default.item_default import ItemDefault

		brand: DF.Data
		brand_defaults: DF.Table[ItemDefault]
		description: DF.Text | None
		image: DF.AttachImage | None
	# end: auto-generated types

	pass


def get_brand_defaults(item, company):
	item = artech_engine.get_cached_doc("Item", item)
	if item.brand:
		brand = artech_engine.get_cached_doc("Brand", item.brand)

		for d in brand.brand_defaults or []:
			if d.company == company:
				row = d.as_dict(no_private_properties=True)
				row.pop("name")
				return row

	return artech_engine._dict()
