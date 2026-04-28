import artech_engine
from artech_engine.query_builder.functions import IfNull


def execute():
	update_delivery_note()
	update_pick_list_items()


def update_delivery_note():
	DN = artech_engine.qb.DocType("Delivery Note")
	DNI = artech_engine.qb.DocType("Delivery Note Item")

	artech_engine.qb.update(DNI).join(DN).on(DN.name == DNI.parent).set(DNI.against_pick_list, DN.pick_list).where(
		IfNull(DN.pick_list, "") != ""
	).run()


def update_pick_list_items():
	PL = artech_engine.qb.DocType("Pick List")
	PLI = artech_engine.qb.DocType("Pick List Item")

	pick_lists = artech_engine.qb.from_(PL).select(PL.name).where(PL.status == "Completed").run(pluck="name")

	if not pick_lists:
		return

	artech_engine.qb.update(PLI).set(PLI.delivered_qty, PLI.picked_qty).where(PLI.parent.isin(pick_lists)).run()
