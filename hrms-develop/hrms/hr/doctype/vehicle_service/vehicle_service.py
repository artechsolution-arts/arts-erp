# For license information, please see license.txt


from artech_engine.model.document import Document


class VehicleService(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		expense_amount: DF.Currency
		frequency: DF.Literal["", "Mileage", "Monthly", "Quarterly", "Half Yearly", "Yearly"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		service_item: DF.Link
		type: DF.Literal["", "Inspection", "Service", "Change"]
	# end: auto-generated types

	pass
