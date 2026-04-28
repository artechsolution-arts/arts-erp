# Copyright (c) 2020, Artech and contributors
# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class EmailDigestRecipient(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		recipient: DF.Link
	# end: auto-generated types

	pass
