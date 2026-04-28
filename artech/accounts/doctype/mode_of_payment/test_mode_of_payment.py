# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestModeofPayment(ArtechTestSuite):
	pass


def set_default_account_for_mode_of_payment(mode_of_payment, company, account):
	mode_of_payment.reload()
	if artech_engine.db.exists(
		"Mode of Payment Account", {"parent": mode_of_payment.mode_of_payment, "company": company}
	):
		artech_engine.db.set_value(
			"Mode of Payment Account",
			{"parent": mode_of_payment.mode_of_payment, "company": company},
			"default_account",
			account,
		)
		return

	mode_of_payment.append("accounts", {"company": company, "default_account": account})
	mode_of_payment.save()
