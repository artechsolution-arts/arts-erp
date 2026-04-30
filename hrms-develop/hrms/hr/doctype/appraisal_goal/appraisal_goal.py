from artech_engine.model.document import Document


class AppraisalGoal(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		kra: DF.SmallText
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		per_weightage: DF.Float
		score: DF.Float
		score_earned: DF.Float
	# end: auto-generated types

	pass
