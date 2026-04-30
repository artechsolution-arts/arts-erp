import artech_engine
from artech_engine.query_builder import DocType


def execute():
	"""
	Description:
	Call set_total_advance_paid for advance ledger entries
	"""
	advance_doctpyes = ["Employee Advance", "Leave Encashment", "Gratuity"]

	for doctype in advance_doctpyes:
		if artech_engine.db.has_table(doctype):
			call_set_total_advance_paid(doctype)


def call_set_total_advance_paid(doctype) -> list:
	aple = DocType("Advance Payment Ledger Entry")
	advance_doctype = DocType(doctype)

	date = artech_engine.utils.getdate("31-07-2025")

	entries = (
		artech_engine.qb.from_(aple)
		.left_join(advance_doctype)
		.on(aple.against_voucher_no == advance_doctype.name)
		.select(aple.against_voucher_no, aple.against_voucher_type)
		.where((aple.delinked == 0) & (advance_doctype.creation >= date))
	).run(as_dict=True)

	for entry in entries:
		try:
			advance_payment_ledger = artech_engine.get_doc(entry.against_voucher_type, entry.against_voucher_no)
			advance_payment_ledger.set_total_advance_paid()
		except Exception as e:
			artech_engine.log_error(e)
			continue
