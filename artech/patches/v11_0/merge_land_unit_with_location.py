import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	# Rename and reload the Land Unit and Linked Land Unit doctypes
	if artech_engine.db.table_exists("Land Unit") and not artech_engine.db.table_exists("Location"):
		artech_engine.rename_doc("DocType", "Land Unit", "Location", force=True)

	artech_engine.reload_doc("assets", "doctype", "location")

	if artech_engine.db.table_exists("Linked Land Unit") and not artech_engine.db.table_exists("Linked Location"):
		artech_engine.rename_doc("DocType", "Linked Land Unit", "Linked Location", force=True)

	artech_engine.reload_doc("assets", "doctype", "linked_location")

	if not artech_engine.db.table_exists("Crop Cycle"):
		artech_engine.reload_doc("agriculture", "doctype", "crop_cycle")

	# Rename the fields in related doctypes
	if "linked_land_unit" in artech_engine.db.get_table_columns("Crop Cycle"):
		rename_field("Crop Cycle", "linked_land_unit", "linked_location")

	if "land_unit" in artech_engine.db.get_table_columns("Linked Location"):
		rename_field("Linked Location", "land_unit", "location")

	if not artech_engine.db.exists("Location", "All Land Units"):
		artech_engine.get_doc({"doctype": "Location", "is_group": True, "location_name": "All Land Units"}).insert(
			ignore_permissions=True
		)

	if artech_engine.db.table_exists("Land Unit"):
		land_units = artech_engine.get_all("Land Unit", fields=["*"], order_by="lft")

		for land_unit in land_units:
			if not artech_engine.db.exists("Location", land_unit.get("land_unit_name")):
				artech_engine.get_doc(
					{
						"doctype": "Location",
						"location_name": land_unit.get("land_unit_name"),
						"parent_location": land_unit.get("parent_land_unit") or "All Land Units",
						"is_container": land_unit.get("is_container"),
						"is_group": land_unit.get("is_group"),
						"latitude": land_unit.get("latitude"),
						"longitude": land_unit.get("longitude"),
						"area": land_unit.get("area"),
						"location": land_unit.get("location"),
						"lft": land_unit.get("lft"),
						"rgt": land_unit.get("rgt"),
					}
				).insert(ignore_permissions=True)

	# Delete the Land Unit and Linked Land Unit doctypes
	if artech_engine.db.table_exists("Land Unit"):
		artech_engine.delete_doc("DocType", "Land Unit", force=1)

	if artech_engine.db.table_exists("Linked Land Unit"):
		artech_engine.delete_doc("DocType", "Linked Land Unit", force=1)
