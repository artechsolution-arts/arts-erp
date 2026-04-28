# Copyright (c) 2017, Artech and contributors
# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document


class Driver(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.setup.doctype.driving_license_category.driving_license_category import (
			DrivingLicenseCategory,
		)

		address: DF.Link | None
		cell_number: DF.Data | None
		driving_license_category: DF.Table[DrivingLicenseCategory]
		employee: DF.Link | None
		expiry_date: DF.Date | None
		full_name: DF.Data
		issuing_date: DF.Date | None
		license_number: DF.Data | None
		naming_series: DF.Literal["HR-DRI-.YYYY.-"]
		status: DF.Literal["Active", "Suspended", "Left"]
		transporter: DF.Link | None
	# end: auto-generated types

	def validate(self):
		if self.employee:
			self.user = artech_engine.get_value("Employee", self.employee, "user_id")
