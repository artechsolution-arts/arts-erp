# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt


import json

import artech_engine
from artech_engine import _, throw
from artech_engine.model.document import Document
from artech_engine.utils import cint
from artech_engine.utils.jinja import validate_template


class TermsandConditions(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		buying: DF.Check
		disabled: DF.Check
		selling: DF.Check
		terms: DF.TextEditor | None
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		if self.terms:
			validate_template(self.terms)
		if not cint(self.buying) and not cint(self.selling) and not cint(self.hr) and not cint(self.disabled):
			throw(_("At least one of the Applicable Modules should be selected"))


@artech_engine.whitelist()
def get_terms_and_conditions(template_name: str, doc: str | dict):
	if isinstance(doc, str):
		doc = json.loads(doc)

	terms_and_conditions = artech_engine.get_doc("Terms and Conditions", template_name)

	if terms_and_conditions.terms:
		return artech_engine.render_template(terms_and_conditions.terms, doc)
