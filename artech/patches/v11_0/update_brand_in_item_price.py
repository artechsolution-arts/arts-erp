# Copyright (c) 2015, Artech and Contributors


import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "item_price")

	artech_engine.db.sql(
		""" update `tabItem Price`, `tabItem`
		set
			`tabItem Price`.brand = `tabItem`.brand
		where
			`tabItem Price`.item_code = `tabItem`.name
			and `tabItem`.brand is not null and `tabItem`.brand != ''"""
	)
