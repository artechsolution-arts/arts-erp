# For license information, please see license.txt

# import artech_engine
from artech_engine.model.document import Document


class JobOfferTermTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from hrms.hr.doctype.job_offer_term.job_offer_term import JobOfferTerm

		offer_terms: DF.Table[JobOfferTerm]
		title: DF.Data | None
	# end: auto-generated types

	pass
