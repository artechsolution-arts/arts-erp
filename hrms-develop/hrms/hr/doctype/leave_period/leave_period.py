# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.utils import getdate

from hrms.hr.utils import validate_overlap


class LeavePeriod(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		company: DF.Link
		from_date: DF.Date
		is_active: DF.Check
		optional_holiday_list: DF.Link | None
		to_date: DF.Date
	# end: auto-generated types

	def validate(self):
		self.validate_dates()
		validate_overlap(self, self.from_date, self.to_date, self.company)

	def validate_dates(self):
		if getdate(self.from_date) >= getdate(self.to_date):
			artech_engine.throw(_("To date can not be equal or less than from date"))
