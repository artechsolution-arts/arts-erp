# See license.txt

import artech_engine

from artech.setup.doctype.employee.test_employee import make_employee

from artech_hrms.payroll.doctype.employee_tax_exemption_declaration.test_employee_tax_exemption_declaration import (
	PAYROLL_PERIOD_END,
	PAYROLL_PERIOD_NAME,
	PAYROLL_PERIOD_START,
	create_exemption_category,
	create_payroll_period,
	setup_hra_exemption_prerequisites,
)
from artech_hrms.tests.utils import HRMSTestSuite


class TestEmployeeTaxExemptionProofSubmission(HRMSTestSuite):
	def setUp(self):
		artech_engine.db.delete("Employee Tax Exemption Proof Submission")
		artech_engine.db.delete("Salary Structure Assignment")

		make_employee("employee@proofsubmission.com", company="_Test Company")
		create_payroll_period(
			company="_Test Company",
			name=PAYROLL_PERIOD_NAME,
			start_date=PAYROLL_PERIOD_START,
			end_date=PAYROLL_PERIOD_END,
		)

		create_exemption_category()

	def test_exemption_amount_lesser_than_category_max(self):
		proof = artech_engine.get_doc(
			{
				"doctype": "Employee Tax Exemption Proof Submission",
				"employee": artech_engine.get_value("Employee", {"user_id": "employee@proofsubmission.com"}, "name"),
				"payroll_period": "Test Payroll Period",
				"tax_exemption_proofs": [
					dict(
						exemption_sub_category="_Test Sub Category",
						type_of_proof="Test Proof",
						exemption_category="_Test Category",
						amount=150000,
					)
				],
			}
		)
		self.assertRaises(artech_engine.ValidationError, proof.save)
		proof = artech_engine.get_doc(
			{
				"doctype": "Employee Tax Exemption Proof Submission",
				"payroll_period": "Test Payroll Period",
				"employee": artech_engine.get_value("Employee", {"user_id": "employee@proofsubmission.com"}, "name"),
				"tax_exemption_proofs": [
					dict(
						exemption_sub_category="_Test Sub Category",
						type_of_proof="Test Proof",
						exemption_category="_Test Category",
						amount=100000,
					)
				],
			}
		)
		self.assertTrue(proof.save)
		self.assertTrue(proof.submit)

	def test_duplicate_category_in_proof_submission(self):
		proof = artech_engine.get_doc(
			{
				"doctype": "Employee Tax Exemption Proof Submission",
				"employee": artech_engine.get_value("Employee", {"user_id": "employee@proofsubmission.com"}, "name"),
				"payroll_period": "Test Payroll Period",
				"tax_exemption_proofs": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						type_of_proof="Test Proof",
						amount=100000,
					),
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=50000,
					),
				],
			}
		)
		self.assertRaises(artech_engine.ValidationError, proof.save)

	def test_india_hra_exemption(self):
		# set country
		current_country = artech_engine.flags.country
		artech_engine.flags.country = "India"

		employee = artech_engine.get_value("Employee", {"user_id": "employee@proofsubmission.com"}, "name")
		setup_hra_exemption_prerequisites("Monthly", employee)

		proof = artech_engine.get_doc(
			{
				"doctype": "Employee Tax Exemption Proof Submission",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": PAYROLL_PERIOD_NAME,
				"currency": "INR",
				"house_rent_payment_amount": 600000,
				"rented_in_metro_city": 1,
				"rented_from_date": PAYROLL_PERIOD_START,
				"rented_to_date": PAYROLL_PERIOD_END,
				"tax_exemption_proofs": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						type_of_proof="Test Proof",
						amount=100000,
					),
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						type_of_proof="Test Proof",
						amount=50000,
					),
				],
			}
		).insert()

		self.assertEqual(proof.monthly_house_rent, 50000)

		# Monthly HRA received = 3000
		# should set HRA exemption as per actual annual HRA because that's the minimum
		self.assertEqual(proof.monthly_hra_exemption, 3000)
		self.assertEqual(proof.total_eligible_hra_exemption, 36000)

		# total exemptions + house rent payment amount
		self.assertEqual(proof.total_actual_amount, 750000)

		# 100000 Standard Exemption + 36000 HRA exemption
		self.assertEqual(proof.exemption_amount, 136000)

		# reset
		artech_engine.flags.country = current_country
