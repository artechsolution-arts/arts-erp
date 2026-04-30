# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class EmployeeOtherIncome(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amended_from: DF.Link | None
		amount: DF.Currency
		company: DF.Link
		employee: DF.Link
		employee_name: DF.Data | None
		payroll_period: DF.Link
		source: DF.Data | None
	# end: auto-generated types

	pass
