# Copyright (c) 2015, Artech and Contributors


from artech_engine.model.document import Document


class UOM(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		category: DF.Link | None
		common_code: DF.Data | None
		description: DF.SmallText | None
		enabled: DF.Check
		must_be_whole_number: DF.Check
		symbol: DF.Data | None
		uom_name: DF.Data
	# end: auto-generated types

	pass
