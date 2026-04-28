from artech import encode_company_abbr
from artech.tests.utils import ArtechTestSuite


class TestInit(ArtechTestSuite):
	def test_encode_company_abbr(self):
		abbr = "NFECT"

		names = [
			"Warehouse Name",
			"Artech Foundation India",
			f"Gold - Member - {abbr}",
			f" - {abbr}",
			"Artech - Foundation - India",
			f"Artech Foundation India - {abbr}",
			f"No-Space-{abbr}",
			"- Warehouse",
		]

		expected_names = [
			f"Warehouse Name - {abbr}",
			f"Artech Foundation India - {abbr}",
			f"Gold - Member - {abbr}",
			f" - {abbr}",
			f"Artech - Foundation - India - {abbr}",
			f"Artech Foundation India - {abbr}",
			f"No-Space-{abbr} - {abbr}",
			f"- Warehouse - {abbr}",
		]

		for i in range(len(names)):
			enc_name = encode_company_abbr(names[i], abbr=abbr)
			self.assertTrue(
				enc_name == expected_names[i],
				f"{enc_name} is not same as {expected_names[i]}",
			)

	def test_translation_files(self):
		from artech_engine.tests.test_translate import verify_translation_files

		verify_translation_files("artech")

	def test_patches(self):
		from artech_engine.tests.test_patches import check_patch_files

		check_patch_files("artech")
