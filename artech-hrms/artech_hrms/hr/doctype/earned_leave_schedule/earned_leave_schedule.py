# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class EarnedLeaveSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		allocated_via: DF.Literal["", "Scheduler", "Leave Policy Assignment", "Manually"]
		allocation_date: DF.Date | None
		attempted: DF.Check
		failed: DF.Check
		failure_reason: DF.SmallText | None
		is_allocated: DF.Check
		number_of_leaves: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
