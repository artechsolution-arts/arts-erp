# Copyright (c) 2025, Artech and contributors
# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class WorkstationOperatingComponent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.manufacturing.doctype.workstation_operating_component_account.workstation_operating_component_account import (
			WorkstationOperatingComponentAccount,
		)

		accounts: DF.Table[WorkstationOperatingComponentAccount]
		component_name: DF.Data
	# end: auto-generated types

	pass
