# Copyright (c) 2015, Artech and Contributors


import artech_engine


def execute():
	artech_engine.db.sql(
		"""update tabItem set variant_based_on = 'Item Attribute'
		where ifnull(variant_based_on, '') = ''
		and (has_variants=1 or ifnull(variant_of, '') != '')
	"""
	)
