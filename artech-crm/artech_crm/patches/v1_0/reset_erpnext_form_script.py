import artech_engine

from artech_crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings import get_crm_form_script


def execute():
	reset_erpnext_form_script()


def reset_erpnext_form_script():
	try:
		if artech_engine.db.exists("CRM Form Script", "Create Quotation from CRM Deal"):
			script = get_crm_form_script()
			artech_engine.db.set_value("CRM Form Script", "Create Quotation from CRM Deal", "script", script)
			return True
		return False
	except Exception:
		artech_engine.log_error(artech_engine.get_traceback(), "Error while resetting form script")
		return False
