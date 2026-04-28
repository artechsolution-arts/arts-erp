import artech_engine
from artech_engine import _
from artech_engine.model.utils.rename_field import rename_field
from artech_engine.utils.nestedset import rebuild_tree


def execute():
	if artech_engine.db.table_exists("Supplier Group"):
		artech_engine.reload_doc("setup", "doctype", "supplier_group")
	elif artech_engine.db.table_exists("Supplier Type"):
		artech_engine.rename_doc("DocType", "Supplier Type", "Supplier Group", force=True)
		artech_engine.reload_doc("setup", "doctype", "supplier_group")
		artech_engine.reload_doc("accounts", "doctype", "pricing_rule")
		artech_engine.reload_doc("accounts", "doctype", "tax_rule")
		artech_engine.reload_doc("buying", "doctype", "buying_settings")
		artech_engine.reload_doc("buying", "doctype", "supplier")
		rename_field("Supplier Group", "supplier_type", "supplier_group_name")
		rename_field("Supplier", "supplier_type", "supplier_group")
		rename_field("Buying Settings", "supplier_type", "supplier_group")
		rename_field("Pricing Rule", "supplier_type", "supplier_group")
		rename_field("Tax Rule", "supplier_type", "supplier_group")

	build_tree()


def build_tree():
	artech_engine.db.sql(
		"""update `tabSupplier Group` set parent_supplier_group = '{}'
		where is_group = 0""".format(_("All Supplier Groups"))
	)

	if not artech_engine.db.exists("Supplier Group", _("All Supplier Groups")):
		artech_engine.get_doc(
			{
				"doctype": "Supplier Group",
				"supplier_group_name": _("All Supplier Groups"),
				"is_group": 1,
				"parent_supplier_group": "",
			}
		).insert(ignore_permissions=True)

	rebuild_tree("Supplier Group")
