# Copyright (c) 2020, Artech and Contributors
# MIT License. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "Payment Schedule")
	if artech_engine.db.count("Payment Schedule"):
		artech_engine.db.sql(
			"""
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		"""
		)
