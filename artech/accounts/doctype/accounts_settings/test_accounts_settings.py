import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestAccountsSettings(ArtechTestSuite):
	def test_stale_days(self):
		cur_settings = artech_engine.get_doc("Accounts Settings", "Accounts Settings")
		cur_settings.allow_stale = 0
		cur_settings.stale_days = 0

		self.assertRaises(artech_engine.ValidationError, cur_settings.save)

		cur_settings.stale_days = -1
		self.assertRaises(artech_engine.ValidationError, cur_settings.save)
