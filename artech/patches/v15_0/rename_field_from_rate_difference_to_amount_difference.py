import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	artech_engine.db.set_value(
		"DocField",
		{"parent": "Purchase Receipt Item", "fieldname": "rate_difference_with_purchase_invoice"},
		"label",
		"Amount Difference with Purchase Invoice",
	)
	rename_field(
		"Purchase Receipt Item",
		"rate_difference_with_purchase_invoice",
		"amount_difference_with_purchase_invoice",
	)
	artech_engine.clear_cache(doctype="Purchase Receipt Item")
