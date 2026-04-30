# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document
from artech_engine.utils.data import comma_and


class FacebookLeadForm(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from crm.lead_syncing.doctype.facebook_lead_form_question.facebook_lead_form_question import (
			FacebookLeadFormQuestion,
		)

		form_name: DF.Data | None
		id: DF.Data | None
		page: DF.Link
		questions: DF.Table[FacebookLeadFormQuestion]
	# end: auto-generated types

	def validate(self):
		self.check_mandatory_crm_fields_mapped()

	def check_mandatory_crm_fields_mapped(self):
		# right now only first name is mandatory
		# later this can be elaborated to use doctype meta
		mandatory_crm_lead_fields = [{"label": "First Name", "fieldname": "first_name"}]
		mandatory_crm_lead_fieldnames = set(f["fieldname"] for f in mandatory_crm_lead_fields)

		if self.is_new():
			return

		mapped_fields = set(q.mapped_to_crm_field for q in self.questions)
		not_mapped = list(mandatory_crm_lead_fieldnames.difference(mapped_fields))

		if not_mapped:
			not_mapped_labels = [
				f["label"] for f in mandatory_crm_lead_fields if f["fieldname"] in not_mapped
			]
			formatted_fields_list = artech_engine.bold(comma_and(not_mapped_labels))
			artech_engine.throw(artech_engine._("Mandatory field(s) {0} must be mapped").format(formatted_fields_list))
