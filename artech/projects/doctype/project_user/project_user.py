# Copyright (c) 2015, Artech and contributors
# For license information, please see license.txt


from artech_engine.model.document import Document


class ProjectUser(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		email: DF.ReadOnly | None
		full_name: DF.ReadOnly | None
		image: DF.ReadOnly | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project_status: DF.Text | None
		user: DF.Link
		view_attachments: DF.Check
		welcome_email_sent: DF.Check
	# end: auto-generated types

	pass
