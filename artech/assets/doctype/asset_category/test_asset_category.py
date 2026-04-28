# See license.txt

import artech_engine

from artech.assets.doctype.asset.test_asset import create_asset
from artech.tests.utils import ArtechTestSuite


class TestAssetCategory(ArtechTestSuite):
	def test_mandatory_fields(self):
		asset_category = artech_engine.new_doc("Asset Category")
		asset_category.asset_category_name = "Computers"

		self.assertRaises(artech_engine.MandatoryError, asset_category.insert)

		asset_category.total_number_of_depreciations = 3
		asset_category.frequency_of_depreciation = 3
		asset_category.append(
			"accounts",
			{
				"company_name": "_Test Company",
				"fixed_asset_account": "_Test Fixed Asset - _TC",
				"accumulated_depreciation_account": "_Test Accumulated Depreciations - _TC",
				"depreciation_expense_account": "_Test Depreciations - _TC",
			},
		)

		try:
			asset_category.insert(ignore_if_duplicate=True)
		except artech_engine.DuplicateEntryError:
			pass

	def test_cwip_accounting(self):
		artech_engine.db.get_value("Company", "_Test Company", "capital_work_in_progress_account")
		artech_engine.db.set_value("Company", "_Test Company", "capital_work_in_progress_account", "")

		asset_category = artech_engine.new_doc("Asset Category")
		asset_category.asset_category_name = "Computers"
		asset_category.enable_cwip_accounting = 1

		asset_category.total_number_of_depreciations = 3
		asset_category.frequency_of_depreciation = 3
		asset_category.append(
			"accounts",
			{
				"company_name": "_Test Company",
				"fixed_asset_account": "_Test Fixed Asset - _TC",
				"accumulated_depreciation_account": "_Test Accumulated Depreciations - _TC",
				"depreciation_expense_account": "_Test Depreciations - _TC",
			},
		)

		self.assertRaises(artech_engine.ValidationError, asset_category.insert)

	def test_duplicate_company_accounts(self):
		asset_category = artech_engine.get_doc(
			{
				"doctype": "Asset Category",
				"asset_category_name": "Computers",
				"accounts": [
					{
						"company_name": "_Test Company",
						"fixed_asset_account": "_Test Fixed Asset - _TC",
					},
					{
						"company_name": "_Test Company",
						"fixed_asset_account": "_Test Fixed Asset - _TC",
					},
				],
			}
		)
		with self.assertRaises(artech_engine.ValidationError) as err:
			asset_category.save()
		self.assertTrue("Cannot set multiple account rows for the same company" in str(err.exception))

	def test_depreciation_accounts_required_for_existing_depreciable_assets(self):
		asset = create_asset(
			asset_category="Computers",
			calculate_depreciation=1,
			company="_Test Company",
			submit=1,
		)
		company_acccount_depreciation = artech_engine.db.get_value(
			"Company",
			asset.company,
			[
				"accumulated_depreciation_account",
				"depreciation_expense_account",
			],
			as_dict=True,
		)
		artech_engine.db.set_value(
			"Company",
			asset.company,
			{
				"accumulated_depreciation_account": "",
				"depreciation_expense_account": "",
			},
		)
		try:
			asset_category = artech_engine.get_doc("Asset Category", asset.asset_category)
			asset_category.enable_cwip_accounting = 0
			for row in asset_category.accounts:
				if row.company_name == asset.company and (
					row.accumulated_depreciation_account or row.depreciation_expense_account
				):
					row.accumulated_depreciation_account = None
					row.depreciation_expense_account = None
			with self.assertRaises(artech_engine.ValidationError) as err:
				asset_category.save()

			self.assertTrue(
				"Since there are active depreciable assets under this category, the following accounts are required."
				in str(err.exception)
			)
		finally:
			artech_engine.db.set_value("Company", asset.company, company_acccount_depreciation)
