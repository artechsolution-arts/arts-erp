# Copyright(c) 2020, Artech Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "stock_entry")
	if artech_engine.db.has_column("Stock Entry", "add_to_transit"):
		artech_engine.db.sql(
			"""
            UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer',
            add_to_transit = 1 WHERE stock_entry_type = 'Send to Warehouse'
            """
		)

		artech_engine.db.sql(
			"""UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer'
            WHERE stock_entry_type = 'Receive at Warehouse'
            """
		)

		artech_engine.reload_doc("stock", "doctype", "warehouse_type")
		if not artech_engine.db.exists("Warehouse Type", "Transit"):
			doc = artech_engine.new_doc("Warehouse Type")
			doc.name = "Transit"
			doc.insert()

		artech_engine.reload_doc("stock", "doctype", "stock_entry_type")
		artech_engine.delete_doc_if_exists("Stock Entry Type", "Send to Warehouse")
		artech_engine.delete_doc_if_exists("Stock Entry Type", "Receive at Warehouse")
