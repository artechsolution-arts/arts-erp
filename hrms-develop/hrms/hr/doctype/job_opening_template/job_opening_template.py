# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document
from artech_engine.model.mapper import get_mapped_doc


class JobOpeningTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		department: DF.Link | None
		description: DF.TextEditor | None
		employment_type: DF.Link | None
		location: DF.Link | None
		template_title: DF.Data
	# end: auto-generated types

	pass


@artech_engine.whitelist()
def create_job_opening_from_template(source: str | Document) -> Document:
	target_doc = artech_engine.new_doc("Job Opening")

	def set_missing_values(source_doc, target_doc):
		target_doc.job_title = source_doc.designation

	doc = get_mapped_doc(
		"Job Opening Template",
		source,
		{
			"Job Opening Template": {"doctype": "Job Opening"},
			"field_map": {
				"name": "job_opening_template",
			},
		},
		target_doc,
		set_missing_values,
	)
	return doc
