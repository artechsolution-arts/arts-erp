import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	# updating column value to handle field change from Data to Currency
	changed_field = "base_scrap_material_cost"
	artech_engine.db.sql(f"update `tabBOM` set {changed_field} = '0' where trim(coalesce({changed_field}, ''))= ''")

	for doctype in ["BOM Explosion Item", "BOM Item", "Work Order Item", "Item"]:
		if artech_engine.db.has_column(doctype, "allow_transfer_for_manufacture"):
			if doctype != "Item":
				artech_engine.reload_doc("manufacturing", "doctype", artech_engine.scrub(doctype))
			else:
				artech_engine.reload_doc("stock", "doctype", artech_engine.scrub(doctype))

			rename_field(doctype, "allow_transfer_for_manufacture", "include_item_in_manufacturing")

	for doctype in ["BOM", "Work Order"]:
		artech_engine.reload_doc("manufacturing", "doctype", artech_engine.scrub(doctype))

		if artech_engine.db.has_column(doctype, "transfer_material_against_job_card"):
			artech_engine.db.sql(
				""" UPDATE `tab%s`
                SET transfer_material_against = CASE WHEN
                    transfer_material_against_job_card = 1 then 'Job Card' Else 'Work Order' END
                WHERE docstatus < 2"""
				% (doctype)
			)
		else:
			artech_engine.db.sql(
				""" UPDATE `tab%s`
                SET transfer_material_against = 'Work Order'
                WHERE docstatus < 2"""
				% (doctype)
			)
