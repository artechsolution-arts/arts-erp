# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class AppointmentLettercontent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		description: DF.LongText
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		title: DF.Data
	# end: auto-generated types

	pass
