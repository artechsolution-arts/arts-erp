# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt

import artech_engine


def create_designation(**args):
	args = artech_engine._dict(args)
	if artech_engine.db.exists("Designation", args.designation_name or "_Test designation"):
		return artech_engine.get_doc("Designation", args.designation_name or "_Test designation")

	designation = artech_engine.get_doc(
		{
			"doctype": "Designation",
			"designation_name": args.designation_name or "_Test designation",
			"description": args.description or "_Test description",
		}
	)
	designation.save()
	return designation
