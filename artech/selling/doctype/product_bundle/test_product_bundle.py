# Copyright (c) 2015, Artech and Contributors

import artech_engine


def make_product_bundle(parent, items, qty=None):
	if artech_engine.db.exists("Product Bundle", parent):
		return artech_engine.get_doc("Product Bundle", parent)

	product_bundle = artech_engine.get_doc({"doctype": "Product Bundle", "new_item_code": parent})

	for item in items:
		product_bundle.append("items", {"item_code": item, "qty": qty or 1})

	product_bundle.insert()

	return product_bundle
