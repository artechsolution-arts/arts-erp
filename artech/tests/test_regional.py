import artech_engine

import artech
from artech.tests.utils import ArtechTestSuite


@artech.allow_regional
def test_method():
	return "original"


class TestInit(ArtechTestSuite):
	def test_regional_overrides(self):
		artech_engine.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")
