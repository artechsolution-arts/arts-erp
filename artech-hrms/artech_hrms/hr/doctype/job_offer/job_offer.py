# For license information, please see license.txt


import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.model.mapper import get_mapped_doc
from artech_engine.utils import cint, flt, get_link_to_form


class JobOffer(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from hrms.hr.doctype.job_offer_term.job_offer_term import JobOfferTerm

		amended_from: DF.Link | None
		applicant_email: DF.Data | None
		applicant_name: DF.Data
		company: DF.Link
		designation: DF.Link
		job_applicant: DF.Link
		job_offer_term_template: DF.Link | None
		letter_head: DF.Link | None
		offer_date: DF.Date
		offer_terms: DF.Table[JobOfferTerm]
		select_print_heading: DF.Link | None
		select_terms: DF.Link | None
		status: DF.Literal["Awaiting Response", "Accepted", "Rejected", "Cancelled"]
		terms: DF.TextEditor | None
	# end: auto-generated types

	def onload(self):
		employee = artech_engine.db.get_value("Employee", {"job_applicant": self.job_applicant}, "name") or ""
		self.set_onload("employee", employee)

	def validate(self):
		self.validate_vacancies()
		job_offer = artech_engine.db.exists(
			"Job Offer", {"job_applicant": self.job_applicant, "docstatus": ["!=", 2]}
		)
		if job_offer and job_offer != self.name:
			artech_engine.throw(
				_("Job Offer: {0} is already for Job Applicant: {1}").format(
					artech_engine.bold(job_offer), artech_engine.bold(self.job_applicant)
				)
			)

	def validate_vacancies(self):
		staffing_plan = get_staffing_plan_detail(self.designation, self.company, self.offer_date)
		check_vacancies = artech_engine.get_single("HR Settings").check_vacancies
		if staffing_plan and check_vacancies:
			job_offers = self.get_job_offer(staffing_plan.from_date, staffing_plan.to_date)
			if not staffing_plan.get("vacancies") or cint(staffing_plan.vacancies) - len(job_offers) <= 0:
				error_variable = "for " + artech_engine.bold(self.designation)
				if staffing_plan.get("parent"):
					error_variable = artech_engine.bold(get_link_to_form("Staffing Plan", staffing_plan.parent))

				artech_engine.throw(_("There are no vacancies under staffing plan {0}").format(error_variable))

	def on_change(self):
		update_job_applicant(self.status, self.job_applicant)

	def get_job_offer(self, from_date, to_date):
		"""Returns job offer created during a time period"""
		return artech_engine.get_all(
			"Job Offer",
			filters={
				"offer_date": ["between", (from_date, to_date)],
				"designation": self.designation,
				"company": self.company,
				"docstatus": 1,
			},
			fields=["name"],
		)

	def on_discard(self):
		self.db_set("status", "Cancelled")


def update_job_applicant(status, job_applicant):
	if status in ("Accepted", "Rejected"):
		artech_engine.set_value("Job Applicant", job_applicant, "status", status)


def get_staffing_plan_detail(designation, company, offer_date):
	detail = artech_engine.db.sql(
		"""
		SELECT DISTINCT spd.parent,
			sp.from_date as from_date,
			sp.to_date as to_date,
			sp.name,
			sum(spd.vacancies) as vacancies,
			spd.designation
		FROM `tabStaffing Plan Detail` spd, `tabStaffing Plan` sp
		WHERE
			sp.docstatus=1
			AND spd.designation=%s
			AND sp.company=%s
			AND spd.parent = sp.name
			AND %s between sp.from_date and sp.to_date
	""",
		(designation, company, offer_date),
		as_dict=1,
	)

	return artech_engine._dict(detail[0]) if (detail and detail[0].parent) else None


@artech_engine.whitelist()
def make_employee(source_name: str, target_doc: str | Document | None = None):
	def set_missing_values(source, target):
		target.personal_email, target.first_name = artech_engine.db.get_value(
			"Job Applicant", source.job_applicant, ["email_id", "applicant_name"]
		)

	doc = get_mapped_doc(
		"Job Offer",
		source_name,
		{
			"Job Offer": {
				"doctype": "Employee",
				"field_map": {"applicant_name": "employee_name", "offer_date": "scheduled_confirmation_date"},
			}
		},
		target_doc,
		set_missing_values,
	)
	return doc


@artech_engine.whitelist()
def get_offer_acceptance_rate(company: str | None = None, department: str | None = None):
	artech_engine.has_permission("Job Offer", throw=True)

	filters = {"docstatus": 1}
	if company:
		filters["company"] = company
	if department:
		filters["department"] = department

	total_offers = artech_engine.db.count("Job Offer", filters=filters)

	filters["status"] = "Accepted"
	total_accepted = artech_engine.db.count("Job Offer", filters=filters)

	return {
		"value": flt(total_accepted) / flt(total_offers) * 100 if total_offers else 0,
		"fieldtype": "Percent",
	}
