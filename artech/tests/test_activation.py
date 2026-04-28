from artech.tests.utils import ArtechTestSuite
from artech.utilities.activation import get_level


class TestActivation(ArtechTestSuite):
	def test_activation(self):
		site_info = {"activation": {"activation_level": 0, "sales_data": []}}
		levels = get_level(site_info)
		self.assertTrue(levels)
