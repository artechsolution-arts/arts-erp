# Copyright (c) 2018, Artech and contributors
# For license information, please see license.txt


import json

import artech_engine
from artech_engine.model.document import Document
from artech_engine.utils.jinja import validate_template


class ContractTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech.crm.doctype.contract_template_fulfilment_terms.contract_template_fulfilment_terms import (
			ContractTemplateFulfilmentTerms,
		)

		contract_terms: DF.TextEditor | None
		fulfilment_terms: DF.Table[ContractTemplateFulfilmentTerms]
		requires_fulfilment: DF.Check
		title: DF.Data | None
	# end: auto-generated types

	def validate(self):
		if self.contract_terms:
			validate_template(self.contract_terms)


@artech_engine.whitelist()
def get_contract_template(template_name: str, doc: str | dict | Document):
	if isinstance(doc, str):
		doc = json.loads(doc)

	contract_template = artech_engine.get_doc("Contract Template", template_name)
	contract_terms = None

	if contract_template.contract_terms:
		contract_terms = artech_engine.render_template(contract_template.contract_terms, doc)

	return {"contract_template": contract_template, "contract_terms": contract_terms}
