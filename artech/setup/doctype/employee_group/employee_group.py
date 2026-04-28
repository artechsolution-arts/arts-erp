# Copyright (c) 2018, Artech and contributors
# For license information, please see license.txt


from artech_engine.model.document import Document


class EmployeeGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.setup.doctype.employee_group_table.employee_group_table import EmployeeGroupTable

		employee_group_name: DF.Data
		employee_list: DF.Table[EmployeeGroupTable]
	# end: auto-generated types

	pass
