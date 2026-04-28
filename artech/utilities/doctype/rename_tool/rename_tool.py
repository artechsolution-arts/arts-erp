# Copyright (c) 2015, Artech and Contributors

# For license information, please see license.txt


import artech_engine
from artech_engine.model.document import Document
from artech_engine.model.rename_doc import bulk_rename
from artech_engine.utils.deprecations import deprecated


class RenameTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		file_to_rename: DF.Attach | None
		select_doctype: DF.Link | None
	# end: auto-generated types

	pass


@artech_engine.whitelist()
@deprecated
def get_doctypes():
	return artech_engine.db.sql_list(
		"""select name from tabDocType
		where allow_rename=1 and module!='Core' order by name"""
	)


@artech_engine.whitelist()
def upload(select_doctype: str | None = None):
	from artech_engine.utils.csvutils import read_csv_content_from_attached_file

	if not select_doctype:
		select_doctype = artech_engine.form_dict.select_doctype

	if not artech_engine.has_permission(select_doctype, "write"):
		raise artech_engine.PermissionError

	rows = read_csv_content_from_attached_file(artech_engine.get_doc("Rename Tool", "Rename Tool"))

	# bulk rename allows only 500 rows at a time, so we created one job per 500 rows
	for i in range(0, len(rows), 500):
		artech_engine.enqueue(
			method=bulk_rename,
			queue="long",
			doctype=select_doctype,
			rows=rows[i : i + 500],
		)
