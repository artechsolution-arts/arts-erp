# Copyright (c) 2018, Artech and contributors
# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import cint, flt


class Routing(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.manufacturing.doctype.bom_operation.bom_operation import BOMOperation

		disabled: DF.Check
		operations: DF.Table[BOMOperation]
		routing_name: DF.Data | None
	# end: auto-generated types

	def validate(self):
		self.calculate_operating_cost()
		self.set_routing_id()

	def on_update(self):
		self.calculate_operating_cost()

	def calculate_operating_cost(self):
		for operation in self.operations:
			if not operation.hour_rate:
				operation.hour_rate = artech_engine.db.get_value("Workstation", operation.workstation, "hour_rate")
			operation.operating_cost = flt(
				flt(operation.hour_rate) * flt(operation.time_in_mins) / 60,
				operation.precision("operating_cost"),
			)

	def set_routing_id(self):
		sequence_id = 0
		for row in self.operations:
			if not row.sequence_id:
				row.sequence_id = sequence_id + 1
			elif sequence_id and row.sequence_id and cint(sequence_id) > cint(row.sequence_id):
				artech_engine.throw(
					_(
						"At row #{0}: the sequence id {1} cannot be less than previous row sequence id {2}"
					).format(row.idx, row.sequence_id, sequence_id)
				)

			sequence_id = row.sequence_id


@artech_engine.whitelist()
@artech_engine.validate_and_sanitize_search_inputs
def get_operations(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict):
	query_filters = {}

	if txt:
		query_filters = {"operation": ["like", f"%{txt}%"]}

	if filters.get("routing"):
		query_filters["parent"] = filters.get("routing")

	return artech_engine.get_all(
		"BOM Operation",
		fields=["operation"],
		filters=query_filters,
		start=start,
		page_length=page_len,
		as_list=1,
	)
