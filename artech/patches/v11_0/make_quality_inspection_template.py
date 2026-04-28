# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine


def execute():
	artech_engine.reload_doc("stock", "doctype", "quality_inspection_template")
	artech_engine.reload_doc("stock", "doctype", "item")

	for data in artech_engine.get_all(
		"Item Quality Inspection Parameter", fields=["parent"], filters={"parenttype": "Item"}, distinct=True
	):
		qc_doc = artech_engine.new_doc("Quality Inspection Template")
		qc_doc.quality_inspection_template_name = "QIT/%s" % data.parent
		qc_doc.flags.ignore_mandatory = True
		qc_doc.save(ignore_permissions=True)

		artech_engine.db.set_value(
			"Item", data.parent, "quality_inspection_template", qc_doc.name, update_modified=False
		)
		artech_engine.db.sql(
			""" update `tabItem Quality Inspection Parameter`
			set parentfield = 'item_quality_inspection_parameter', parenttype = 'Quality Inspection Template',
			parent = %s where parenttype = 'Item' and parent = %s""",
			(qc_doc.name, data.parent),
		)

	# update field in item variant settings
	artech_engine.db.sql(
		""" update `tabVariant Field` set field_name = 'quality_inspection_template'
		where field_name = 'quality_parameters'"""
	)
