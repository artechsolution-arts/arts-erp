# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.query_builder import Criterion
from artech_engine.utils import get_link_to_form


class ProductBundle(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.selling.doctype.product_bundle_item.product_bundle_item import ProductBundleItem

		description: DF.Data | None
		disabled: DF.Check
		items: DF.Table[ProductBundleItem]
		new_item_code: DF.Link
	# end: auto-generated types

	def autoname(self):
		self.name = self.new_item_code

	def validate(self):
		self.validate_main_item()
		self.validate_child_items()
		self.validate_child_items_qty_non_zero()
		from artech.utilities.transaction_base import validate_uom_is_integer

		validate_uom_is_integer(self, "uom", "qty")

	def on_trash(self):
		linked_doctypes = [
			"Delivery Note",
			"Sales Invoice",
			"POS Invoice",
			"Purchase Receipt",
			"Purchase Invoice",
			"Stock Entry",
			"Stock Reconciliation",
			"Sales Order",
			"Purchase Order",
			"Material Request",
		]

		invoice_links = []
		for doctype in linked_doctypes:
			item_doctype = doctype + " Item"

			if doctype == "Stock Entry":
				item_doctype = doctype + " Detail"

			invoices = artech_engine.db.get_all(
				item_doctype, {"item_code": self.new_item_code, "docstatus": 1}, ["parent"]
			)

			for invoice in invoices:
				invoice_links.append(get_link_to_form(doctype, invoice["parent"]))

		if len(invoice_links):
			artech_engine.throw(
				"This Product Bundle is linked with {}. You will have to cancel these documents in order to delete this Product Bundle".format(
					", ".join(invoice_links)
				),
				title=_("Not Allowed"),
			)

	def validate_main_item(self):
		"""Validates, main Item is not a stock item"""
		if artech_engine.db.get_value("Item", self.new_item_code, "is_stock_item"):
			artech_engine.throw(_("Parent Item {0} must not be a Stock Item").format(self.new_item_code))
		if artech_engine.db.get_value("Item", self.new_item_code, "is_fixed_asset"):
			artech_engine.throw(_("Parent Item {0} must not be a Fixed Asset").format(self.new_item_code))

	def validate_child_items(self):
		for item in self.items:
			if artech_engine.db.exists("Product Bundle", {"name": item.item_code, "disabled": 0}):
				artech_engine.throw(
					_(
						"Row #{0}: Child Item should not be a Product Bundle. Please remove Item {1} and Save"
					).format(item.idx, artech_engine.bold(item.item_code))
				)

	def validate_child_items_qty_non_zero(self):
		for item in self.items:
			if item.qty <= 0:
				artech_engine.throw(
					_(
						"Row #{0}: Quantity cannot be a non-positive number. Please increase the quantity or remove the Item {1}"
					).format(item.idx, artech_engine.bold(item.item_code))
				)


@artech_engine.whitelist()
@artech_engine.validate_and_sanitize_search_inputs
def get_new_item_code(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict):
	product_bundles = artech_engine.db.get_list("Product Bundle", {"disabled": 0}, pluck="name")

	if not searchfield or searchfield == "name":
		searchfield = artech_engine.get_meta("Item").get("search_fields")

	searchfield = searchfield.split(",")
	searchfield.append("name")

	item = artech_engine.qb.DocType("Item")
	query = (
		artech_engine.qb.from_(item)
		.select(item.name, item.item_name)
		.where((item.is_stock_item == 0) & (item.is_fixed_asset == 0))
		.limit(page_len)
		.offset(start)
	)

	if searchfield:
		query = query.where(Criterion.any([item[fieldname].like(f"%{txt}%") for fieldname in searchfield]))

	if product_bundles:
		query = query.where(item.name.notin(product_bundles))

	return query.run()
