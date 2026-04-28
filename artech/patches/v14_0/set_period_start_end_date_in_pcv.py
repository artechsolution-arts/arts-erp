# Copyright (c) 2023, Artech and Contributors
# License: MIT. See LICENSE


import artech_engine


def execute():
	# nosemgrep
	artech_engine.db.sql(
		"""
		UPDATE `tabPeriod Closing Voucher`
		SET
			period_start_date = (select year_start_date from `tabFiscal Year` where name = fiscal_year),
			period_end_date = posting_date
	"""
	)
