# See license.txt

import artech_engine
from artech_engine.utils import add_days, nowdate

from artech.setup.doctype.designation.test_designation import create_designation

from artech_hrms.hr.doctype.job_applicant.job_applicant import get_applicant_to_hire_percentage
from artech_hrms.hr.doctype.job_offer.job_offer import get_offer_acceptance_rate
from artech_hrms.hr.doctype.staffing_plan.test_staffing_plan import make_company
from artech_hrms.tests.test_utils import create_job_applicant
from artech_hrms.tests.utils import HRMSTestSuite


class TestJobOffer(HRMSTestSuite):
	def setUp(self):
		create_designation(designation_name="Researcher")

	def test_job_offer_creation_against_vacancies(self):
		artech_engine.db.set_single_value("HR Settings", "check_vacancies", 1)
		job_applicant = create_job_applicant(email_id="test_job_offer@example.com")
		job_offer = create_job_offer(job_applicant=job_applicant.name, designation="UX Designer")

		create_staffing_plan(
			name="Test No Vacancies",
			staffing_details=[
				{"designation": "UX Designer", "vacancies": 0, "estimated_cost_per_position": 5000}
			],
			company="_Test Company",
		)
		self.assertRaises(artech_engine.ValidationError, job_offer.submit)

		# test creation of job offer when vacancies are not present
		artech_engine.db.set_single_value("HR Settings", "check_vacancies", 0)
		job_offer.submit()
		self.assertTrue(artech_engine.db.exists("Job Offer", job_offer.name))

	def test_job_applicant_update(self):
		artech_engine.db.set_single_value("HR Settings", "check_vacancies", 0)
		create_staffing_plan()
		job_applicant = create_job_applicant(email_id="test_job_applicants@example.com")
		job_offer = create_job_offer(job_applicant=job_applicant.name)
		job_offer.submit()
		job_applicant.reload()
		self.assertEqual(job_applicant.status, "Accepted")

		# status update after rejection
		job_offer.status = "Rejected"
		job_offer.submit()
		job_applicant.reload()
		self.assertEqual(job_applicant.status, "Rejected")
		artech_engine.db.set_single_value("HR Settings", "check_vacancies", 1)

	def test_recruitment_metrics(self):
		job_applicant1 = create_job_applicant(email_id="test_job_applicant1@example.com")
		job_applicant2 = create_job_applicant(email_id="test_job_applicant2@example.com")
		job_offer = create_job_offer(job_applicant=job_applicant1.name)
		job_offer.status = "Accepted"
		job_offer.submit()

		self.assertEqual(get_applicant_to_hire_percentage().get("value"), 50)

		job_offer = create_job_offer(job_applicant=job_applicant2.name)
		job_offer.status = "Rejected"
		job_offer.submit()

		self.assertEqual(get_offer_acceptance_rate().get("value"), 50)

	def test_status_on_save(self):
		job_offer = create_job_offer()
		job_offer.save()
		job_offer.discard()
		job_offer.reload()
		self.assertEqual(job_offer.status, "Cancelled")


def create_job_offer(**args):
	args = artech_engine._dict(args)
	if not args.job_applicant:
		job_applicant = create_job_applicant()

	if not artech_engine.db.exists("Designation", args.designation):
		create_designation(designation_name=args.designation)

	job_offer = artech_engine.get_doc(
		{
			"doctype": "Job Offer",
			"job_applicant": args.job_applicant or job_applicant.name,
			"offer_date": args.offer_date or nowdate(),
			"designation": args.designation or "Researcher",
			"status": args.status or "Accepted",
			"company": args.company or "_Test Company",
		}
	)
	job_offer.update(args)
	return job_offer


def create_staffing_plan(**args):
	args = artech_engine._dict(args)
	make_company()
	artech_engine.db.set_value("Company", "_Test Company", "is_group", 1)
	if artech_engine.db.exists("Staffing Plan", args.name or "Test"):
		return
	staffing_plan = artech_engine.get_doc(
		{
			"doctype": "Staffing Plan",
			"name": args.name or "Test",
			"from_date": args.from_date or nowdate(),
			"to_date": args.to_date or add_days(nowdate(), 10),
			"staffing_details": args.staffing_details
			or [{"designation": "Researcher", "vacancies": 1, "estimated_cost_per_position": 50000}],
			"company": args.company or "_Test Company",
		}
	)
	staffing_plan.insert()
	staffing_plan.submit()
	return staffing_plan
