import artech_engine
from artech_engine import qb
from pypika.functions import Replace


def execute():
	sp = artech_engine.qb.DocType("Sales Partner")
	qb.update(sp).set(sp.partner_website, Replace(sp.partner_website, "http://", "https://")).where(
		sp.partner_website.rlike("^http://.*")
	).run()
