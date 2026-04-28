# For license information, please see license.txt


from artech_engine.model.document import Document


class QualityAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.quality_management.doctype.quality_action_resolution.quality_action_resolution import (
			QualityActionResolution,
		)

		corrective_preventive: DF.Literal["Corrective", "Preventive"]
		date: DF.Date | None
		feedback: DF.Link | None
		goal: DF.Link | None
		procedure: DF.Link | None
		resolutions: DF.Table[QualityActionResolution]
		review: DF.Link | None
		status: DF.Literal["Open", "Completed"]
	# end: auto-generated types

	def validate(self):
		self.status = "Open" if any([d.status == "Open" for d in self.resolutions]) else "Completed"
