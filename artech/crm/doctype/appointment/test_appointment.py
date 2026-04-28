# Copyright (c) 2019, Artech and Contributors
# See license.txt
import datetime

import artech_engine

from artech.tests.utils import ArtechTestSuite

LEAD_EMAIL = "test_appointment_lead@example.com"


def create_test_appointment():
	test_appointment = artech_engine.get_doc(
		{
			"doctype": "Appointment",
			"status": "Open",
			"customer_name": "Test Lead",
			"customer_phone_number": "666",
			"customer_skype": "test",
			"customer_email": LEAD_EMAIL,
			"scheduled_time": datetime.datetime.now(),
			"customer_details": "Hello, Friend!",
		}
	)
	test_appointment.insert()
	return test_appointment


class TestAppointment(ArtechTestSuite):
	def setUp(self):
		artech_engine.db.delete("Lead", {"email_id": LEAD_EMAIL})
		self.test_appointment = create_test_appointment()
		self.test_appointment.set_verified(self.test_appointment.customer_email)

	def test_calendar_event_created(self):
		cal_event = artech_engine.get_doc("Event", self.test_appointment.calendar_event)
		self.assertEqual(cal_event.starts_on, self.test_appointment.scheduled_time)

	def test_lead_linked(self):
		self.assertTrue(self.test_appointment.party)
