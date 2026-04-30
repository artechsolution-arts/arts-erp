# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class PayrollPeriodDate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		end_date: DF.Date
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		start_date: DF.Date
	# end: auto-generated types

	pass
