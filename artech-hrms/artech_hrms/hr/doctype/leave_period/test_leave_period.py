# See license.txt

import artech_engine

import artech

from artech_hrms.tests.utils import HRMSTestSuite


def create_leave_period(from_date, to_date, company=None):
	leave_period = artech_engine.db.get_value(
		"Leave Period",
		dict(
			company=company or "_Test Company",
			from_date=from_date,
			to_date=to_date,
			is_active=1,
		),
		"name",
	)
	if leave_period:
		return artech_engine.get_doc("Leave Period", leave_period)

	leave_period = artech_engine.get_doc(
		{
			"doctype": "Leave Period",
			"company": company or "_Test Company",
			"from_date": from_date,
			"to_date": to_date,
			"is_active": 1,
		}
	).insert()
	return leave_period
