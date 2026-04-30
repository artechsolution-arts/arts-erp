# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import flt


class EmployeeTaxExemptionSubCategory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		exemption_category: DF.Link
		is_active: DF.Check
		max_amount: DF.Currency
	# end: auto-generated types

	def validate(self):
		category_max_amount = artech_engine.db.get_value(
			"Employee Tax Exemption Category", self.exemption_category, "max_amount"
		)
		if flt(self.max_amount) > flt(category_max_amount):
			artech_engine.throw(
				_(
					"Max Exemption Amount cannot be greater than maximum exemption amount {0} of Tax Exemption Category {1}"
				).format(category_max_amount, self.exemption_category)
			)
