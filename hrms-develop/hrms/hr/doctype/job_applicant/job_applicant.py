# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.model.naming import append_number_if_name_exists
from artech_engine.utils import flt, validate_email_address

from hrms.hr.doctype.interview.interview import get_interviewers


class DuplicationError(artech_engine.ValidationError):
	pass


class JobApplicant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		applicant_name: DF.Data
		applicant_rating: DF.Rating
		country: DF.Link | None
		cover_letter: DF.Text | None
		currency: DF.Link | None
		designation: DF.Link | None
		email_id: DF.Data
		employee_referral: DF.Link | None
		job_title: DF.Link | None
		lower_range: DF.Currency
		notes: DF.Data | None
		phone_number: DF.Data | None
		resume_attachment: DF.Attach | None
		resume_link: DF.Data | None
		source: DF.Link | None
		source_name: DF.Link | None
		status: DF.Literal["Open", "Replied", "Shortlisted", "Rejected", "Hold", "Accepted"]
		upper_range: DF.Currency
	# end: auto-generated types

	def onload(self):
		job_offer = artech_engine.get_all("Job Offer", filters={"job_applicant": self.name})
		if job_offer:
			self.get("__onload").job_offer = job_offer[0].name

	def autoname(self):
		self.name = self.email_id

		# applicant can apply more than once for a different job title or reapply
		if artech_engine.db.exists("Job Applicant", self.name):
			self.name = append_number_if_name_exists("Job Applicant", self.name)

	def validate(self):
		if self.email_id:
			validate_email_address(self.email_id, True)

		if self.employee_referral:
			self.set_status_for_employee_referral()

		if not self.applicant_name and self.email_id:
			guess = self.email_id.split("@")[0]
			self.applicant_name = " ".join([p.capitalize() for p in guess.split(".")])

	def before_insert(self):
		if self.job_title:
			job_opening_status = artech_engine.db.get_value("Job Opening", self.job_title, "status")
			if job_opening_status == "Closed":
				artech_engine.throw(
					_("Cannot create a Job Applicant against a closed Job Opening"), title=_("Not Allowed")
				)

	def set_status_for_employee_referral(self):
		emp_ref = artech_engine.get_doc("Employee Referral", self.employee_referral)
		if self.status in ["Open", "Replied", "Hold"]:
			emp_ref.db_set("status", "In Process")
		elif self.status in ["Accepted", "Rejected"]:
			emp_ref.db_set("status", self.status)


@artech_engine.whitelist()
def create_interview(job_applicant: str, interview_type: str) -> Document:
	doc = artech_engine.get_doc("Job Applicant", job_applicant)

	round_designation = artech_engine.db.get_value("Interview Type", interview_type, "designation")

	if round_designation and doc.designation and round_designation != doc.designation:
		artech_engine.throw(
			_("Interview Type {0} is only applicable for the Designation {1}").format(
				interview_type, round_designation
			)
		)

	interview = artech_engine.new_doc("Interview")
	interview.interview_type = interview_type
	interview.job_applicant = doc.name
	interview.designation = doc.designation
	interview.resume_link = doc.resume_link
	interview.job_opening = doc.job_title

	interviewers = get_interviewers(interview_type)
	for d in interviewers:
		interview.append("interview_details", {"interviewer": d.interviewer})

	return interview


@artech_engine.whitelist()
def get_interview_details(job_applicant: str) -> dict:
	interview_details = artech_engine.db.get_all(
		"Interview",
		filters={"job_applicant": job_applicant, "docstatus": ["!=", 2]},
		fields=["name", "interview_type", "scheduled_on", "average_rating", "status"],
	)
	if not interview_details:
		return None

	interview_detail_map = {}
	meta = artech_engine.get_meta("Interview")
	number_of_stars = meta.get_options("average_rating") or 5

	for detail in interview_details:
		detail.average_rating = detail.average_rating * number_of_stars if detail.average_rating else 0

		interview_detail_map[detail.name] = detail

	return {"interviews": interview_detail_map, "stars": number_of_stars}


@artech_engine.whitelist()
def get_applicant_to_hire_percentage() -> dict:
	artech_engine.has_permission("Job Applicant", throw=True)

	total_applicants = artech_engine.db.count("Job Applicant")
	total_hired = artech_engine.db.count("Job Applicant", filters={"status": "Accepted"})

	return {
		"value": flt(total_hired) / flt(total_applicants) * 100 if total_applicants else 0,
		"fieldtype": "Percent",
	}
