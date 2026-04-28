# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class AdvanceTaxesandCharges(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		account_head: DF.Link
		add_deduct_tax: DF.Literal["Add", "Deduct"]
		base_net_amount: DF.Currency
		base_tax_amount: DF.Currency
		base_total: DF.Currency
		charge_type: DF.Literal[
			"", "Actual", "On Paid Amount", "On Previous Row Amount", "On Previous Row Total"
		]
		cost_center: DF.Link | None
		currency: DF.Link | None
		description: DF.SmallText
		included_in_paid_amount: DF.Check
		is_tax_withholding_account: DF.Check
		net_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project: DF.Link | None
		rate: DF.Float
		row_id: DF.Data | None
		set_by_item_tax_template: DF.Check
		tax_amount: DF.Currency
		total: DF.Currency
	# end: auto-generated types

	pass
