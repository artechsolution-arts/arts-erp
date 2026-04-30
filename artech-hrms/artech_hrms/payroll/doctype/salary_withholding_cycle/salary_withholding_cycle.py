# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class SalaryWithholdingCycle(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from_date: DF.Date
		is_salary_released: DF.Check
		journal_entry: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		to_date: DF.Date
	# end: auto-generated types

	pass
