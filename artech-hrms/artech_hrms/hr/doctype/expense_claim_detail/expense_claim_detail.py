from artech_engine.model.document import Document


class ExpenseClaimDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amount: DF.Currency
		base_amount: DF.Currency
		base_sanctioned_amount: DF.Currency
		cost_center: DF.Link | None
		default_account: DF.Link | None
		description: DF.TextEditor | None
		expense_date: DF.Date | None
		expense_type: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project: DF.Link | None
		sanctioned_amount: DF.Currency
	# end: auto-generated types

	pass
