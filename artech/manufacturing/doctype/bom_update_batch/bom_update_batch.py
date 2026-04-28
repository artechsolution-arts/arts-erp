# Copyright (c) 2022, Artech and contributors
# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class BOMUpdateBatch(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		batch_no: DF.Int
		boms_updated: DF.LongText | None
		level: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		status: DF.Literal["Pending", "Completed"]
	# end: auto-generated types

	pass
