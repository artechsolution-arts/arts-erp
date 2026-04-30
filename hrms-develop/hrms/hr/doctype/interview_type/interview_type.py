# For license information, please see license.txt


import json

import artech_engine
from artech_engine.model.document import Document


class InterviewType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		description: DF.Text | None
	# end: auto-generated types

	pass


@artech_engine.whitelist()
def create_interview(docname: str):
	interview_type = artech_engine.get_doc("Interview Type", docname)

	interview = artech_engine.new_doc("Interview")
	interview.interview_type = interview_type.name
	interview.designation = interview_type.designation

	if interview_type.interviewers:
		interview.interview_details = []
		for d in interview_type.interviewers:
			interview.append("interview_details", {"interviewer": d.user})

	return interview
