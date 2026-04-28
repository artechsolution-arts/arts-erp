# Copyright (c) 2015, Artech and Contributors and contributors
# For license information, please see license.txt


import artech_engine
from dateutil.relativedelta import relativedelta
from artech_engine.model.document import Document
from artech_engine.utils import cint


class ManufacturingSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		add_corrective_operation_cost_in_finished_good_valuation: DF.Check
		allow_editing_of_items_and_quantities_in_work_order: DF.Check
		allow_overtime: DF.Check
		allow_production_on_holidays: DF.Check
		backflush_raw_materials_based_on: DF.Literal["BOM", "Material Transferred for Manufacture"]
		capacity_planning_for_days: DF.Int
		disable_capacity_planning: DF.Check
		enforce_time_logs: DF.Check
		get_rm_cost_from_consumption_entry: DF.Check
		job_card_excess_transfer: DF.Check
		make_serial_no_batch_from_work_order: DF.Check
		material_consumption: DF.Check
		mins_between_operations: DF.Int
		overproduction_percentage_for_sales_order: DF.Percent
		overproduction_percentage_for_work_order: DF.Percent
		set_op_cost_and_secondary_items_from_sub_assemblies: DF.Check
		transfer_extra_materials_percentage: DF.Percent
		update_bom_costs_automatically: DF.Check
		validate_components_quantities_per_bom: DF.Check
	# end: auto-generated types

	def before_save(self):
		self.reset_values()

	def reset_values(self):
		if self.backflush_raw_materials_based_on != "BOM" and self.validate_components_quantities_per_bom:
			self.validate_components_quantities_per_bom = 0


def get_mins_between_operations():
	return relativedelta(
		minutes=cint(artech_engine.db.get_single_value("Manufacturing Settings", "mins_between_operations")) or 10
	)


@artech_engine.whitelist()
def is_material_consumption_enabled():
	if not hasattr(artech_engine.local, "material_consumption"):
		artech_engine.local.material_consumption = cint(
			artech_engine.db.get_single_value("Manufacturing Settings", "material_consumption")
		)

	return artech_engine.local.material_consumption
