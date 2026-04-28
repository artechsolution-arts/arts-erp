# See license.txt


import artech_engine

from artech.stock.doctype.item_attribute.item_attribute import ItemAttributeIncrementError
from artech.tests.utils import ArtechTestSuite


class TestItemAttribute(ArtechTestSuite):
	def setUp(self):
		super().setUp()
		if artech_engine.db.exists("Item Attribute", "_Test_Length"):
			artech_engine.delete_doc("Item Attribute", "_Test_Length")

	def test_numeric_item_attribute(self):
		item_attribute = artech_engine.get_doc(
			{
				"doctype": "Item Attribute",
				"attribute_name": "_Test_Length",
				"numeric_values": 1,
				"from_range": 0.0,
				"to_range": 100.0,
				"increment": 0,
			}
		)

		self.assertRaises(ItemAttributeIncrementError, item_attribute.save)

		item_attribute.increment = 0.5
		item_attribute.save()
