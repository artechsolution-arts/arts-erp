# For license information, please see license.txt


import artech_engine
from artech_engine.model.document import Document


class PaymentGatewayAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		company: DF.Link
		currency: DF.ReadOnly | None
		is_default: DF.Check
		message: DF.SmallText | None
		payment_account: DF.Link
		payment_channel: DF.Literal["", "Email", "Phone"]
		payment_gateway: DF.Link
	# end: auto-generated types

	def autoname(self):
		abbr = artech_engine.db.get_value("Company", self.company, "abbr")
		self.name = self.payment_gateway + " - " + self.currency + " - " + abbr

	def validate(self):
		self.currency = artech_engine.get_cached_value("Account", self.payment_account, "account_currency")

		self.update_default_payment_gateway()
		self.set_as_default_if_not_set()

	def update_default_payment_gateway(self):
		if self.is_default:
			artech_engine.db.set_value(
				"Payment Gateway Account",
				{"is_default": 1, "name": ["!=", self.name], "company": self.company},
				"is_default",
				0,
			)

	def set_as_default_if_not_set(self):
		if not artech_engine.db.exists(
			"Payment Gateway Account", {"is_default": 1, "name": ("!=", self.name), "company": self.company}
		):
			self.is_default = 1
