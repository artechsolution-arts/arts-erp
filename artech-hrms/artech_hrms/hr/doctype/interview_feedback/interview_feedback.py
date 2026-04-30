# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.query_builder.functions import Avg
from artech_engine.utils import flt, get_link_to_form, getdate


class InterviewFeedback(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.hr.doctype.skill_assessment.skill_assessment import SkillAssessment

		amended_from: DF.Link | None
		average_rating: DF.Rating
		feedback: DF.Text | None
		interview: DF.Link
		interview_type: DF.Link
		interviewer: DF.Link
		job_applicant: DF.Link | None
		result: DF.Literal["", "Cleared", "Rejected"]
		skill_assessment: DF.Table[SkillAssessment]
	# end: auto-generated types

	def validate(self):
		self.validate_interviewer()
		self.validate_interview_date()
		self.validate_duplicate()
		self.calculate_average_rating()

	def on_submit(self):
		self.update_interview_average_rating()

	def on_cancel(self):
		self.update_interview_average_rating()

	def validate_interviewer(self):
		applicable_interviewers = get_applicable_interviewers(self.interview)
		if self.interviewer not in applicable_interviewers:
			artech_engine.throw(
				_("{0} is not allowed to submit Interview Feedback for the Interview: {1}").format(
					artech_engine.bold(self.interviewer), artech_engine.bold(self.interview)
				)
			)

	def validate_interview_date(self):
		scheduled_date = artech_engine.db.get_value("Interview", self.interview, "scheduled_on")

		if getdate() < getdate(scheduled_date) and self.docstatus == 1:
			artech_engine.throw(
				_("Submission of {0} before {1} is not allowed").format(
					artech_engine.bold(_("Interview Feedback")), artech_engine.bold(_("Interview Scheduled Date"))
				)
			)

	def validate_duplicate(self):
		duplicate_feedback = artech_engine.db.exists(
			"Interview Feedback",
			{"interviewer": self.interviewer, "interview": self.interview, "docstatus": 1},
		)

		if duplicate_feedback:
			artech_engine.throw(
				_(
					"Feedback already submitted for the Interview {0}. Please cancel the previous Interview Feedback {1} to continue."
				).format(self.interview, get_link_to_form("Interview Feedback", duplicate_feedback))
			)

	def calculate_average_rating(self):
		total_rating = 0
		for d in self.skill_assessment:
			if d.rating:
				total_rating += flt(d.rating)

		self.average_rating = flt(
			total_rating / len(self.skill_assessment) if len(self.skill_assessment) else 0
		)

	def update_interview_average_rating(self):
		interview_feedback = artech_engine.qb.DocType("Interview Feedback")
		query = (
			artech_engine.qb.from_(interview_feedback)
			.where((interview_feedback.interview == self.interview) & (interview_feedback.docstatus == 1))
			.select(Avg(interview_feedback.average_rating).as_("average"))
		)
		data = query.run(as_dict=True)
		average_rating = data[0].average

		interview = artech_engine.get_doc("Interview", self.interview)
		interview.db_set("average_rating", average_rating)
		interview.notify_update()


@artech_engine.whitelist()
def get_applicable_interviewers(interview: str) -> list[str]:
	return artech_engine.get_all("Interview Detail", filters={"parent": interview}, pluck="interviewer")
