import artech_engine
from bs4 import BeautifulSoup
from artech_engine import _
from artech_engine.core.api.file import get_max_file_size
from artech_engine.translate import get_all_translations
from artech_engine.utils import cstr, split_emails, validate_email_address

from crm.utils import is_frappe_version


@artech_engine.whitelist(allow_guest=True)
def get_translations():
	if artech_engine.session.user != "Guest":
		language = artech_engine.db.get_value("User", artech_engine.session.user, "language")
	else:
		language = artech_engine.db.get_single_value("System Settings", "language")

	return get_all_translations(language)


@artech_engine.whitelist()
def get_user_signature():
	user = artech_engine.session.user
	user_email_signature = (
		artech_engine.db.get_value(
			"User",
			user,
			"email_signature",
		)
		if user
		else None
	)

	signature = user_email_signature or artech_engine.db.get_value(
		"Email Account",
		{"default_outgoing": 1, "add_signature": 1},
		"signature",
	)

	if not signature:
		return

	soup = BeautifulSoup(signature, "html.parser")
	html_signature = soup.find("div", {"class": "ql-editor read-mode"})
	_signature = None
	if html_signature:
		_signature = html_signature.renderContents()
	content = ""
	if cstr(_signature) or signature:
		content = f'<br><p class="signature">{signature}</p>'
	return content


def check_app_permission():
	if artech_engine.session.user == "Administrator":
		return True

	allowed_modules = []

	if is_frappe_version("15"):
		allowed_modules = artech_engine.config.get_modules_from_all_apps_for_user()
	elif is_frappe_version("16", above=True):
		from artech_engine.utils.modules import get_modules_from_all_apps_for_user

		allowed_modules = get_modules_from_all_apps_for_user()

	allowed_modules = [x["module_name"] for x in allowed_modules]
	if "FCRM" not in allowed_modules:
		return False

	roles = artech_engine.get_roles()
	if any(role in ["System Manager", "Sales User", "Sales Manager"] for role in roles):
		return True

	return False


@artech_engine.whitelist(allow_guest=True)
def accept_invitation(key: str | None = None):
	if not key:
		artech_engine.throw(_("Invalid or expired key"))

	result = artech_engine.db.get_all("CRM Invitation", filters={"key": key}, pluck="name")
	if not result:
		artech_engine.throw(_("Invalid or expired key"))
	invitation = artech_engine.get_doc("CRM Invitation", result[0])
	invitation.accept()
	invitation.reload()

	if invitation.status == "Accepted":
		artech_engine.local.login_manager.login_as(invitation.email)
		artech_engine.local.response["type"] = "redirect"
		artech_engine.local.response["location"] = "/crm"


@artech_engine.whitelist()
def invite_by_email(emails: str, role: str):
	artech_engine.only_for(["Sales Manager", "System Manager"], True)

	user_roles = artech_engine.get_roles(artech_engine.session.user)

	if role == "System Manager" and "System Manager" not in user_roles:
		artech_engine.throw(_("You are not allowed to invite System Managers"), artech_engine.PermissionError)

	if role == "Sales Manager" and "System Manager" not in user_roles:
		artech_engine.throw(_("You are not allowed to invite Sales Managers"), artech_engine.PermissionError)

	if role not in ["System Manager", "Sales Manager", "Sales User"]:
		artech_engine.throw(_("Cannot invite for this role"), artech_engine.PermissionError)

	if not emails:
		return

	email_string = validate_email_address(emails, throw=False)
	email_list = split_emails(email_string)
	if not email_list:
		return
	existing_members = artech_engine.db.get_all("User", filters={"email": ["in", email_list]}, pluck="email")
	existing_invites = artech_engine.db.get_all(
		"CRM Invitation",
		filters={
			"email": ["in", email_list],
			"role": ["in", ["System Manager", "Sales Manager", "Sales User"]],
		},
		pluck="email",
	)

	to_invite = list(set(email_list) - set(existing_members) - set(existing_invites))

	for email in to_invite:
		artech_engine.get_doc(doctype="CRM Invitation", email=email, role=role).insert(ignore_permissions=True)

	return {
		"existing_members": existing_members,
		"existing_invites": existing_invites,
		"to_invite": to_invite,
	}


@artech_engine.whitelist(methods=["DELETE", "POST"])
def delete_attachment(doctype: str, docname: str, file_url: str):
	if not artech_engine.has_permission(doctype, doc=docname, ptype="write"):
		artech_engine.throw(_("You don't have permission to delete this attachment"), artech_engine.PermissionError)

	file_name = artech_engine.db.get_value(
		"File",
		{"file_url": file_url, "attached_to_doctype": doctype, "attached_to_name": docname},
		"name",
	)
	if file_name:
		artech_engine.delete_doc("File", file_name)


@artech_engine.whitelist()
def get_file_uploader_defaults(doctype: str):
	max_number_of_files = None
	make_attachments_public = False
	if doctype:
		meta = artech_engine.get_meta(doctype)
		max_number_of_files = meta.get("max_attachments")
		make_attachments_public = meta.get("make_attachments_public")

	return {
		"allowed_file_types": artech_engine.get_system_settings("allowed_file_extensions"),
		"max_file_size": get_max_file_size(),
		"max_number_of_files": max_number_of_files,
		"make_attachments_public": bool(make_attachments_public),
	}
