# Copyright (c) 2015, Artech and Contributors
# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestOperation(ArtechTestSuite):
	pass


def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = artech_engine._dict(args)

	if not artech_engine.db.exists("Operation", args.operation):
		doc = artech_engine.get_doc(
			{"doctype": "Operation", "name": args.operation, "workstation": args.workstation}
		)
		doc.insert()
		return doc

	return artech_engine.get_doc("Operation", args.operation)
