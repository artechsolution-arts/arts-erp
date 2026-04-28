# Copyright (c) 2015, Artech and Contributors and contributors
# For license information, please see license.txt


from artech_engine.model.document import Document


class TaskDependsOn(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project: DF.Text | None
		subject: DF.Text | None
		task: DF.Link | None
	# end: auto-generated types

	pass
