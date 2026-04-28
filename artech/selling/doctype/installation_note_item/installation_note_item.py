# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


from artech_engine.model.document import Document


class InstallationNoteItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		description: DF.TextEditor | None
		item_code: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		prevdoc_detail_docname: DF.Data | None
		prevdoc_docname: DF.Data | None
		prevdoc_doctype: DF.Data | None
		qty: DF.Float
		serial_and_batch_bundle: DF.Link | None
		serial_no: DF.SmallText | None
	# end: auto-generated types

	pass
