# For license information, please see license.txt


# import artech_engine
from artech_engine.model.document import Document


class AppointmentLetterTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.hr.doctype.appointment_letter_content.appointment_letter_content import (
			AppointmentLettercontent,
		)

		closing_notes: DF.Text | None
		introduction: DF.LongText
		template_name: DF.Data
		terms: DF.Table[AppointmentLettercontent]
	# end: auto-generated types

	pass
