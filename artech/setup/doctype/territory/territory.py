# Copyright (c) 2015, Artech and Contributors


import artech_engine
from artech_engine import _
from artech_engine.utils import flt
from artech_engine.utils.nestedset import NestedSet, get_root_of


class Territory(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.setup.doctype.target_detail.target_detail import TargetDetail

		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_territory: DF.Link | None
		rgt: DF.Int
		targets: DF.Table[TargetDetail]
		territory_manager: DF.Link | None
		territory_name: DF.Data
	# end: auto-generated types

	nsm_parent_field = "parent_territory"

	def validate(self):
		if not self.parent_territory:
			self.parent_territory = get_root_of("Territory")

		for d in self.get("targets") or []:
			if not flt(d.target_qty) and not flt(d.target_amount):
				artech_engine.throw(_("Either target qty or target amount is mandatory"))

	def on_update(self):
		super().on_update()
		self.validate_one_root()


def on_doctype_update():
	artech_engine.db.add_index("Territory", ["lft", "rgt"])
