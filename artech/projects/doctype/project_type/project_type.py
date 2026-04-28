# Copyright (c) 2017, Artech and contributors
# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class ProjectType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		description: DF.Text | None
		project_type: DF.Data
	# end: auto-generated types

	def on_trash(self):
		if self.name == "External":
			artech_engine.throw(_("You cannot delete Project Type 'External'"))
