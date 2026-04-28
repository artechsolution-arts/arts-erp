# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine

from artech.manufacturing.doctype.work_order.work_order import create_job_card


def execute():
	artech_engine.reload_doc("manufacturing", "doctype", "work_order")
	artech_engine.reload_doc("manufacturing", "doctype", "work_order_item")
	artech_engine.reload_doc("manufacturing", "doctype", "job_card")
	artech_engine.reload_doc("manufacturing", "doctype", "job_card_item")

	fieldname = artech_engine.db.get_value(
		"DocField", {"fieldname": "work_order", "parent": "Timesheet"}, "fieldname"
	)
	if not fieldname:
		fieldname = artech_engine.db.get_value(
			"DocField", {"fieldname": "production_order", "parent": "Timesheet"}, "fieldname"
		)
		if not fieldname:
			return

	for d in artech_engine.get_all(
		"Timesheet", filters={fieldname: ["!=", ""], "docstatus": 0}, fields=[fieldname, "name"]
	):
		if d[fieldname]:
			doc = artech_engine.get_doc("Work Order", d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			artech_engine.delete_doc("Timesheet", d.name)
