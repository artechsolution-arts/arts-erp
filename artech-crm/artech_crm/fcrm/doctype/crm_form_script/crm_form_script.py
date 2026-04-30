# For license information, please see license.txt

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class CRMFormScript(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		dt: DF.Link
		enabled: DF.Check
		is_standard: DF.Check
		script: DF.Code | None
		view: DF.Literal["Form", "List"]
	# end: auto-generated types

	def validate(self):
		in_user_env = not (
			artech_engine.flags.in_install
			or artech_engine.flags.in_patch
			or artech_engine.flags.in_test
			or artech_engine.flags.in_fixtures
		)
		if in_user_env and not self.is_new() and self.is_standard and not artech_engine.conf.developer_mode:
			# only enabled can be changed for standard form scripts
			if self.has_value_changed("enabled"):
				enabled_value = self.enabled
				self.reload()
				self.enabled = enabled_value
			else:
				artech_engine.throw(_("You need to be in developer mode to edit a Standard Form Script"))


def get_form_script(dt, view="Form"):
	"""Returns the form script for the given doctype"""
	FormScript = artech_engine.qb.DocType("CRM Form Script")
	query = (
		artech_engine.qb.from_(FormScript)
		.select("script")
		.where(FormScript.dt == dt)
		.where(FormScript.view == view)
		.where(FormScript.enabled == 1)
	)

	doc = query.run(as_dict=True)
	if doc:
		return [d.script for d in doc] if len(doc) > 1 else doc[0].script
	else:
		return None
