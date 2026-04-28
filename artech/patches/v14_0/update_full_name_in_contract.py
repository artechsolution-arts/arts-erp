import artech_engine
from artech_engine import qb


def execute():
	con = qb.DocType("Contract")
	for c in (
		qb.from_(con)
		.select(con.name, con.party_type, con.party_name)
		.where(con.party_full_name.isnull())
		.run(as_dict=True)
	):
		field = c.party_type.lower() + "_name"
		if res := artech_engine.db.get_value(c.party_type, c.party_name, field):
			artech_engine.db.set_value("Contract", c.name, "party_full_name", res)
