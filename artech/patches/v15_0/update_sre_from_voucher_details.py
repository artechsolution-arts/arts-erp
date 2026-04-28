import artech_engine
from artech_engine.query_builder.functions import IfNull


def execute():
	columns = artech_engine.db.get_table_columns("Stock Reservation Entry")

	if set(["against_pick_list", "against_pick_list_item"]).issubset(set(columns)):
		sre = artech_engine.qb.DocType("Stock Reservation Entry")
		(
			artech_engine.qb.update(sre)
			.set(sre.from_voucher_type, "Pick List")
			.set(sre.from_voucher_no, sre.against_pick_list)
			.set(sre.from_voucher_detail_no, sre.against_pick_list_item)
			.where((IfNull(sre.against_pick_list, "") != "") & (IfNull(sre.against_pick_list_item, "") != ""))
		).run()
