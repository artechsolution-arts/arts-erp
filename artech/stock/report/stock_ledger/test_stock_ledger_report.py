# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import artech_engine
from artech_engine.utils import add_days, today

from artech.maintenance.doctype.maintenance_schedule.test_maintenance_schedule import (
	make_serial_item_with_serial,
)
from artech.tests.utils import ArtechTestSuite


class TestStockLedgerReeport(ArtechTestSuite):
	def setUp(self) -> None:
		make_serial_item_with_serial(self, "_Test Stock Report Serial Item")
		self.filters = artech_engine._dict(
			company="_Test Company",
			from_date=today(),
			to_date=add_days(today(), 30),
			item_code=["_Test Stock Report Serial Item"],
		)
