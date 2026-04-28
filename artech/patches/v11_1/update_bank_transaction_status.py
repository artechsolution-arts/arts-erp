# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("accounts", "doctype", "bank_transaction")

	bank_transaction_fields = artech_engine.get_meta("Bank Transaction").get_valid_columns()

	if "debit" in bank_transaction_fields:
		artech_engine.db.sql(
			""" UPDATE `tabBank Transaction`
            SET status = 'Reconciled'
            WHERE
                status = 'Settled' and (debit = allocated_amount or credit = allocated_amount)
                and ifnull(allocated_amount, 0) > 0
        """
		)

	elif "deposit" in bank_transaction_fields:
		artech_engine.db.sql(
			""" UPDATE `tabBank Transaction`
            SET status = 'Reconciled'
            WHERE
                status = 'Settled' and (deposit = allocated_amount or withdrawal = allocated_amount)
                and ifnull(allocated_amount, 0) > 0
        """
		)
