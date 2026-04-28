# Copyright (c) 2019, Artech and Contributors
# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestSellingSettings(ArtechTestSuite):
	def test_defaults_populated(self):
		# Setup default values are not populated on migrate, this test checks
		# if setup was completed correctly
		default = artech_engine.db.get_single_value("Selling Settings", "maintain_same_rate_action")
		self.assertEqual("Stop", default)
