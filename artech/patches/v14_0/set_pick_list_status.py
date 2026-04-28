# Copyright (c) 2023, Artech and Contributors
# License: MIT. See LICENSE


import artech_engine
from pypika.terms import ExistsCriterion


def execute():
	pl = artech_engine.qb.DocType("Pick List")
	se = artech_engine.qb.DocType("Stock Entry")
	dn = artech_engine.qb.DocType("Delivery Note")

	(
		artech_engine.qb.update(pl).set(
			pl.status,
			(
				artech_engine.qb.terms.Case()
				.when(pl.docstatus == 0, "Draft")
				.when(pl.docstatus == 2, "Cancelled")
				.else_("Completed")
			),
		)
	).run()

	(
		artech_engine.qb.update(pl)
		.set(pl.status, "Open")
		.where(
			(
				ExistsCriterion(
					artech_engine.qb.from_(se).select(se.name).where((se.docstatus == 1) & (se.pick_list == pl.name))
				)
				| ExistsCriterion(
					artech_engine.qb.from_(dn).select(dn.name).where((dn.docstatus == 1) & (dn.pick_list == pl.name))
				)
			).negate()
			& (pl.docstatus == 1)
		)
	).run()
