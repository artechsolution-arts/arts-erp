# Copyright (c) 2015, Artech and Contributors


import artech_engine


def execute():
	if artech_engine.db.table_exists("Asset Adjustment") and not artech_engine.db.table_exists("Asset Value Adjustment"):
		artech_engine.rename_doc("DocType", "Asset Adjustment", "Asset Value Adjustment", force=True)
		artech_engine.reload_doc("assets", "doctype", "asset_value_adjustment")
