import artech_engine
from artech_engine import _
from artech_engine.auth import LoginAttemptTracker
from artech_engine.rate_limiter import rate_limit
from artech_engine.utils.password import check_password, update_password


@artech_engine.whitelist()
@rate_limit(limit=5, seconds=300)  # 5 attempts per 5 minutes per user/IP
def change_password(old_password: str, new_password: str):
	"""
	Change password for the current logged-in user.
	Uses Frappe's LoginAttemptTracker for attempt counting/lockout, and rate_limit for API abuse protection.
	"""
	user = artech_engine.session.user
	if user == "Guest":
		artech_engine.throw(_("You must be logged in to change your password"), artech_engine.AuthenticationError)

	tracker = LoginAttemptTracker(user)
	if not tracker.is_user_allowed():
		artech_engine.throw(_("Too many failed attempts. Please try again after some time."))

	if old_password == new_password:
		artech_engine.throw(
			_("New password cannot be the same as current password. Please choose a different password.")
		)

	try:
		check_password(user, old_password)
	except artech_engine.AuthenticationError:
		tracker.add_failure_attempt()
		artech_engine.throw(_("Incorrect current password. Please try again."))
	else:
		tracker.add_success_attempt()

	# Validate new password strength (server-side enforcement)
	from artech_engine.core.doctype.user.user import test_password_strength

	result = test_password_strength(new_password)
	feedback = result.get("feedback", {})
	if not feedback.get("password_policy_validation_passed", False):
		suggestions = feedback.get("suggestions", [])
		artech_engine.throw(_("Password is too weak. {0}").format(" ".join(suggestions) if suggestions else ""))

	update_password(user=user, pwd=new_password, logout_all_sessions=False)
	return _("Password Updated Successfully")


@artech_engine.whitelist()
def add_existing_users(users: str | list, role: str = "Sales User"):
	"""
	Add existing users to the CRM by assigning them a role (Sales User or Sales Manager).
	:param users: List of user names to be added
	"""
	artech_engine.only_for(["System Manager", "Sales Manager"], True)
	is_system_manager = "System Manager" in artech_engine.get_roles()

	if role == "System Manager" and not is_system_manager:
		artech_engine.throw(_("Only System Managers can assign the System Manager role"), artech_engine.PermissionError)

	if role == "Sales Manager" and not is_system_manager:
		artech_engine.throw(_("Only System Managers can assign the Sales Manager role"), artech_engine.PermissionError)

	users = artech_engine.parse_json(users)

	for user in users:
		update_user_role(user, role)


@artech_engine.whitelist()
def update_user_role(user: str, new_role: str):
	"""
	Update the role of the user to Sales Manager, Sales User, or System Manager.
	:param user: The name of the user
	:param new_role: The new role to assign (Sales Manager or Sales User)
	"""

	artech_engine.only_for(["System Manager", "Sales Manager"], True)
	is_system_manager = "System Manager" in artech_engine.get_roles()

	if new_role not in ["System Manager", "Sales Manager", "Sales User"]:
		artech_engine.throw(_("Cannot assign this role"))

	user_doc = artech_engine.get_doc("User", user)
	target_roles = [d.role for d in user_doc.roles]
	target_is_system_manager = "System Manager" in target_roles

	if new_role == "System Manager" and not is_system_manager:
		artech_engine.throw(_("Only System Managers can assign the System Manager role"), artech_engine.PermissionError)

	if target_is_system_manager and not is_system_manager:
		artech_engine.throw(_("Only System Managers can modify other System Managers"), artech_engine.PermissionError)

	if new_role == "Sales Manager" and not is_system_manager:
		artech_engine.throw(_("Only System Managers can assign the Sales Manager role"), artech_engine.PermissionError)

	if new_role == "System Manager":
		user_doc.append_roles("System Manager", "Sales Manager", "Sales User")
		user_doc.set("block_modules", [])
	if new_role == "Sales Manager":
		user_doc.append_roles("Sales Manager", "Sales User")
		remove_roles(user_doc, "System Manager")
	if new_role == "Sales User":
		user_doc.append_roles("Sales User")
		remove_roles(user_doc, "Sales Manager", "System Manager")
		update_module_in_user(user_doc, "FCRM")

	user_doc.save(ignore_permissions=True)


@artech_engine.whitelist()
def remove_crm_roles_from_user(user: str):
	"""
	Remove a user means removing Sales User & Sales Manager roles from the user.
	:param user: The name of the user to be removed
	"""
	artech_engine.only_for(["System Manager", "Sales Manager"], True)

	if user == artech_engine.session.user:
		artech_engine.throw(_("You cannot remove yourself."), artech_engine.PermissionError)

	user_doc = artech_engine.get_doc("User", user)
	roles = [d.role for d in user_doc.roles]

	current_user_is_system_manager = "System Manager" in artech_engine.get_roles()

	if "System Manager" in roles and not current_user_is_system_manager:
		artech_engine.throw(_("Only System Managers can modify other System Managers"), artech_engine.PermissionError)

	if user_doc.get("role_profiles") or user_doc.get("role_profile_name"):
		return artech_engine.throw(
			_("User {0} cannot be removed as it has a Role Profile assigned to it.").format(user)
		)

	if "Sales User" in roles:
		remove_roles(user_doc, "Sales User")
	if "Sales Manager" in roles:
		remove_roles(user_doc, "Sales Manager")

	user_doc.save(ignore_permissions=True)
	artech_engine.msgprint(_("User {0} has been removed from CRM roles.").format(user))


def remove_roles(self, *roles):
	existing_roles = {d.role: d for d in self.get("roles")}
	for role in roles:
		if role in existing_roles:
			self.get("roles").remove(existing_roles[role])


def update_module_in_user(user, module):
	block_modules = artech_engine.get_all(
		"Module Def",
		fields=["name as module"],
		filters={"name": ["!=", module]},
	)

	if block_modules:
		user.set("block_modules", block_modules)
