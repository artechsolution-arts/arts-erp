import artech_engine

from artech.regional.italy import state_codes
from artech.regional.italy.setup import make_custom_fields, setup_report


def execute():
	company = artech_engine.get_all("Company", filters={"country": "Italy"})
	if not company:
		return

	artech_engine.reload_doc("regional", "report", "electronic_invoice_register")
	make_custom_fields()
	setup_report()

	# Set state codes
	condition = ""
	for state, code in state_codes.items():
		condition += f" when {artech_engine.db.escape(state)} then {artech_engine.db.escape(code)}"

	if condition:
		condition = f"state_code = (case state {condition} end),"

	artech_engine.db.sql(
		f"""
		UPDATE tabAddress set {condition} country_code = UPPER(ifnull((select code
			from `tabCountry` where name = `tabAddress`.country), ''))
			where country_code is null and state_code is null
	"""
	)

	artech_engine.db.sql(
		"""
		UPDATE `tabSales Invoice Item` si, `tabSales Order` so
			set si.customer_po_no = so.po_no, si.customer_po_date = so.po_date
		WHERE
			si.sales_order = so.name and so.po_no is not null
	"""
	)
