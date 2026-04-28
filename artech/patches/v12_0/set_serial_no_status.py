import artech_engine
from artech_engine.utils import getdate, nowdate


def execute():
	artech_engine.reload_doc("stock", "doctype", "serial_no")

	serial_no_list = artech_engine.db.sql(
		"""select name, delivery_document_type, warranty_expiry_date, warehouse from `tabSerial No`
		where (status is NULL OR status='')""",
		as_dict=1,
	)
	if len(serial_no_list) > 20000:
		artech_engine.db.auto_commit_on_many_writes = True

	for serial_no in serial_no_list:
		if serial_no.get("delivery_document_type"):
			status = "Delivered"
		elif serial_no.get("warranty_expiry_date") and getdate(
			serial_no.get("warranty_expiry_date")
		) <= getdate(nowdate()):
			status = "Expired"
		elif not serial_no.get("warehouse"):
			status = "Inactive"
		else:
			status = "Active"

		artech_engine.db.set_value("Serial No", serial_no.get("name"), "status", status)

	if artech_engine.db.auto_commit_on_many_writes:
		artech_engine.db.auto_commit_on_many_writes = False
