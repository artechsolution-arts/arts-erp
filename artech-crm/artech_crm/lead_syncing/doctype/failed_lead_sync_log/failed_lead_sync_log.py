# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document

from artech_crm.lead_syncing.doctype.lead_sync_source.facebook import FacebookSyncSource


class FailedLeadSyncLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		lead_data: DF.Code | None
		source: DF.Link | None
		traceback: DF.Code | None
		type: DF.Literal["Duplicate", "Failure", "Synced"]
	# end: auto-generated types

	@artech_engine.whitelist()
	def retry_sync(self):
		if not self.source:
			artech_engine.throw(artech_engine._("Can't retry sync for this without source!"))

		source = artech_engine.get_cached_doc("Lead Sync Source", self.source)
		if source.type != "Facebook":
			artech_engine.throw(artech_engine._("Not implemented yet!"))

		crm_lead = FacebookSyncSource(
			source.get_password("access_token"), source.facebook_lead_form
		).sync_single_lead(artech_engine.parse_json(self.lead_data), raise_exception=True)

		self.type = "Synced"
		self.save()
		return crm_lead
