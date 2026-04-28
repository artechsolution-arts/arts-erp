import artech_engine

from artech.stock.doctype.inventory_dimension.inventory_dimension import get_inventory_dimensions


def execute():
	for dimension in get_inventory_dimensions():
		if artech_engine.db.exists(
			"Custom Field",
			{
				"fieldname": dimension.source_fieldname,
				"dt": "Packed Item",
				"reqd": 1,
			},
		):
			artech_engine.set_value(
				"Custom Field",
				{
					"fieldname": dimension.source_fieldname,
					"dt": "Packed Item",
					"reqd": 1,
				},
				{
					"reqd": 0,
					"mandatory_depends_on": "eval:doc.parent_detail_docname && ['Delivery Note', 'Sales Invoice', 'POS Invoice'].includes(parent.doctype)",
				},
			)
