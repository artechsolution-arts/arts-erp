# Copyright (c) 2020, Artech and contributors
# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class JobCardOperation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		completed_qty: DF.Float
		completed_time: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		status: DF.Literal["Complete", "Pause", "Pending", "Work In Progress"]
		sub_operation: DF.Link | None
	# end: auto-generated types

	pass
