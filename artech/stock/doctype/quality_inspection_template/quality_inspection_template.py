# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import artech_engine
from artech_engine.model.document import Document


class QualityInspectionTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.stock.doctype.item_quality_inspection_parameter.item_quality_inspection_parameter import (
			ItemQualityInspectionParameter,
		)

		item_quality_inspection_parameter: DF.Table[ItemQualityInspectionParameter]
		quality_inspection_template_name: DF.Data
	# end: auto-generated types

	pass


def get_template_details(template):
	if not template:
		return []

	return artech_engine.get_all(
		"Item Quality Inspection Parameter",
		fields=[
			"specification",
			"value",
			"acceptance_formula",
			"numeric",
			"formula_based_criteria",
			"min_value",
			"max_value",
		],
		filters={"parenttype": "Quality Inspection Template", "parent": template},
		order_by="idx",
	)
