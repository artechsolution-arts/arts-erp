# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document

from hrms.hr.utils import set_geolocation_from_coordinates


class ShiftLocation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		checkin_radius: DF.Int
		latitude: DF.Float
		location_name: DF.Data
		longitude: DF.Float
	# end: auto-generated types

	def validate(self):
		self.set_geolocation()

	@artech_engine.whitelist()
	def set_geolocation(self):
		set_geolocation_from_coordinates(self)
