import artech_engine

from artech.setup.doctype.incoterm.incoterm import create_incoterms


def execute():
	create_incoterms()
	migrate_shipments()


def migrate_shipments():
	if not artech_engine.db.count("Shipment"):
		return

	OLD_VALUES = [
		"EXW (Ex Works)",
		"FCA (Free Carrier)",
		"FOB (Free On Board)",
		"FAS (Free Alongside Ship)",
		"CPT (Carriage Paid To)",
		"CIP (Carriage and Insurance Paid to)",
		"CFR (Cost and Freight)",
		"DPU (Delivered At Place Unloaded)",
		"DAP (Delivered At Place)",
		"DDP (Delivered Duty Paid)",
	]
	shipment = artech_engine.qb.DocType("Shipment")
	for old_value in OLD_VALUES:
		artech_engine.qb.update(shipment).set(shipment.incoterm, old_value[:3]).where(
			shipment.incoterm == old_value
		).run()
