# Copyright (c) 2022, Artech and Contributors
# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestWorkstationType(ArtechTestSuite):
	pass


def create_workstation_type(**args):
	args = artech_engine._dict(args)

	if workstation_type := artech_engine.db.exists("Workstation Type", args.workstation_type):
		return artech_engine.get_doc("Workstation Type", workstation_type)
	else:
		doc = artech_engine.new_doc("Workstation Type")
		doc.update(args)
		doc.insert()
		return doc
