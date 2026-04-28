# Copyright (c) 2022, Artech and Contributors
# License: MIT. See LICENSE

import artech_engine


def execute():
	process_soa = artech_engine.qb.DocType("Process Statement Of Accounts")
	q = artech_engine.qb.update(process_soa).set(process_soa.report, "General Ledger")
	q.run()
