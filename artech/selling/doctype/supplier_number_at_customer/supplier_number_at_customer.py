# Copyright (c) 2025, Artech and contributors
# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class SupplierNumberAtCustomer(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		company: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		supplier_number: DF.Data | None
	# end: auto-generated types

	pass
