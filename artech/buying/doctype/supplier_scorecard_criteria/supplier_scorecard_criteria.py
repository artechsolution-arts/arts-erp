# Copyright (c) 2017, Artech and contributors
# For license information, please see license.txt


import re

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document


class InvalidFormulaVariable(artech_engine.ValidationError):
	pass


class SupplierScorecardCriteria(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		criteria_name: DF.Data
		formula: DF.SmallText
		max_score: DF.Float
		weight: DF.Percent
	# end: auto-generated types

	def validate(self):
		self.validate_variables()
		self.validate_formula()

	def validate_variables(self):
		# make sure all the variables exist
		_get_variables(self)

	def validate_formula(self):
		# evaluate the formula with 0's to make sure it is valid
		test_formula = self.formula.replace("\r", "").replace("\n", "")

		regex = r"\{(.*?)\}"

		mylist = re.finditer(regex, test_formula, re.MULTILINE | re.DOTALL)
		for _dummy1, match in enumerate(mylist):
			for _dummy2 in range(0, len(match.groups())):
				test_formula = test_formula.replace("{" + match.group(1) + "}", "1")

		try:
			artech_engine.safe_eval(test_formula, None, {"max": max, "min": min})
		except Exception:
			artech_engine.throw(_("Error evaluating the criteria formula"))


@artech_engine.whitelist()
def get_criteria_list():
	criteria = artech_engine.db.sql(
		"""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Criteria` scs""",
		{},
		as_dict=1,
	)

	return criteria


def get_variables(criteria_name):
	criteria = artech_engine.get_doc("Supplier Scorecard Criteria", criteria_name)
	return _get_variables(criteria)


def _get_variables(criteria):
	my_variables = []
	regex = r"\{(.*?)\}"

	mylist = re.finditer(regex, criteria.formula, re.MULTILINE | re.DOTALL)
	for _dummy1, match in enumerate(mylist):
		for _dummy2 in range(0, len(match.groups())):
			try:
				var = artech_engine.db.sql(
					"""
					SELECT
						scv.variable_label, scv.description, scv.param_name, scv.path
					FROM
						`tabSupplier Scorecard Variable` scv
					WHERE
						param_name=%(param)s""",
					{"param": match.group(1)},
					as_dict=1,
				)[0]
				my_variables.append(var)
			except Exception:
				artech_engine.throw(
					_("Unable to find variable:") + " " + str(match.group(1)), InvalidFormulaVariable
				)

	return my_variables
