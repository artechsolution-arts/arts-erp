# For license information, please see license.txt


from artech_engine.model.document import Document


class EmployeeGrade(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		currency: DF.Link | None
		default_base_pay: DF.Currency
		default_salary_structure: DF.Link | None
	# end: auto-generated types

	pass
