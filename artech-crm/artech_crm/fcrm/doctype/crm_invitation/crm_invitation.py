# For license information, please see license.txt

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class CRMInvitation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		accepted_at: DF.Datetime | None
		email: DF.Data
		email_sent_at: DF.Datetime | None
		invited_by: DF.Link | None
		key: DF.Data | None
		role: DF.Literal["", "Sales User", "Sales Manager", "System Manager"]
		status: DF.Literal["", "Pending", "Accepted", "Expired"]
	# end: auto-generated types

	def before_insert(self):
		artech_engine.utils.validate_email_address(self.email, True)

		self.key = artech_engine.generate_hash(length=12)
		self.invited_by = artech_engine.session.user
		self.status = "Pending"

	def after_insert(self):
		self.invite_via_email()

	def invite_via_email(self):
		invite_link = artech_engine.utils.get_url(f"/api/method/artech_crm.api.accept_invitation?key={self.key}")
		if artech_engine.local.dev_server:
			print(f"Invite link for {self.email}: {invite_link}")  # nosemgrep

		title = "Frappe CRM"
		template = "crm_invitation"

		artech_engine.sendmail(
			recipients=self.email,
			subject=f"You have been invited to join {title}",
			template=template,
			args={"title": title, "invite_link": invite_link},
			now=True,
		)
		self.db_set("email_sent_at", artech_engine.utils.now())

	@artech_engine.whitelist()
	def accept_invitation(self):
		artech_engine.only_for(["System Manager", "Sales Manager"], True)
		self.accept()

	def accept(self):
		if self.status == "Expired":
			artech_engine.throw(_("Invalid or expired key"))

		user = self.create_user_if_not_exists()
		user.append_roles(self.role)
		if self.role == "System Manager":
			user.append_roles("Sales Manager", "Sales User")
		elif self.role == "Sales Manager":
			user.append_roles("Sales User")
		if self.role == "Sales User":
			self.update_module_in_user(user, "FCRM")
		user.save(ignore_permissions=True)

		self.status = "Accepted"
		self.accepted_at = artech_engine.utils.now()
		self.save(ignore_permissions=True)

	def update_module_in_user(self, user, module):
		block_modules = artech_engine.get_all(
			"Module Def",
			fields=["name as module"],
			filters={"name": ["!=", module]},
		)

		if block_modules:
			user.set("block_modules", block_modules)

	def create_user_if_not_exists(self):
		if not artech_engine.db.exists("User", self.email):
			first_name = self.email.split("@")[0].title()
			user = artech_engine.get_doc(
				doctype="User",
				user_type="System User",
				email=self.email,
				send_welcome_email=0,
				first_name=first_name,
			).insert(ignore_permissions=True)
		else:
			user = artech_engine.get_doc("User", self.email)
		return user


def expire_invitations():
	"""expire invitations after 3 days"""
	from artech_engine.utils import add_days, now

	days = 3
	invitations_to_expire = artech_engine.db.get_all(
		"CRM Invitation", filters={"status": "Pending", "creation": ["<", add_days(now(), -days)]}
	)
	for invitation in invitations_to_expire:
		invitation = artech_engine.get_doc("CRM Invitation", invitation.name)
		invitation.status = "Expired"
		invitation.save(ignore_permissions=True)
