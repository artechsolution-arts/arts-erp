import artech_engine


def execute():
	if artech_engine.db.table_exists("Supplier Item Group"):
		artech_engine.reload_doc("selling", "doctype", "party_specific_item")
		sig = artech_engine.db.get_all("Supplier Item Group", fields=["name", "supplier", "item_group"])
		for item in sig:
			psi = artech_engine.new_doc("Party Specific Item")
			psi.party_type = "Supplier"
			psi.party = item.supplier
			psi.restrict_based_on = "Item Group"
			psi.based_on_value = item.item_group
			psi.insert()
