# Copyright (c) 2015, Artech and Contributors


import artech_engine
from artech_engine.contacts.address_and_contact import load_address_and_contact
from artech_engine.utils import cstr, filter_strip_join
from artech_engine.website.website_generator import WebsiteGenerator


class SalesPartner(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.setup.doctype.target_detail.target_detail import TargetDetail

		commission_rate: DF.Float
		description: DF.TextEditor | None
		introduction: DF.Text | None
		logo: DF.Attach | None
		partner_name: DF.Data
		partner_type: DF.Link | None
		partner_website: DF.Data | None
		referral_code: DF.Data | None
		route: DF.Data | None
		show_in_website: DF.Check
		targets: DF.Table[TargetDetail]
		territory: DF.Link
	# end: auto-generated types

	website = artech_engine._dict(
		page_title_field="partner_name",
		condition_field="show_in_website",
		template="templates/generators/sales_partner.html",
	)

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def autoname(self):
		pass

	def validate(self):
		if not self.route:
			self.route = "partners/" + self.scrub(self.partner_name)
		super().validate()
		if self.partner_website:
			from urllib.parse import urlsplit, urlunsplit

			# scrub http
			parts = urlsplit(self.partner_website)
			if not parts.netloc and parts.path:
				parts = parts._replace(netloc=parts.path, path="")
			if not parts.scheme or parts.scheme == "http":
				parts = parts._replace(scheme="https")

			self.partner_website = urlunsplit(parts)

	def get_context(self, context):
		address_names = artech_engine.db.get_all(
			"Dynamic Link",
			filters={"link_doctype": "Sales Partner", "link_name": self.name, "parenttype": "Address"},
			pluck=["parent"],
		)

		addresses = []
		for address_name in address_names:
			address_doc = artech_engine.get_doc("Address", address_name)
			city_state = ", ".join([item for item in [address_doc.city, address_doc.state] if item])
			address_rows = [
				address_doc.address_line1,
				address_doc.address_line2,
				city_state,
				address_doc.pincode,
				address_doc.country,
			]
			addresses.append(
				{
					"email": address_doc.email_id,
					"partner_address": filter_strip_join(address_rows, "\n<br>"),
					"phone": filter_strip_join(cstr(address_doc.phone).split(","), "\n<br>"),
				}
			)

		context["addresses"] = addresses
		return context
