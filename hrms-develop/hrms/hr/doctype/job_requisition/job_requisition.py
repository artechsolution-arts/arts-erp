# For license information, please see license.txt

import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.model.mapper import get_mapped_doc
from artech_engine.utils import format_duration, get_link_to_form, time_diff_in_seconds


class JobRequisition(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		company: DF.Link
		completed_on: DF.Date | None
		department: DF.Link | None
		description: DF.TextEditor
		designation: DF.Link
		expected_by: DF.Date | None
		expected_compensation: DF.Currency
		naming_series: DF.Literal["HR-HIREQ-"]
		no_of_positions: DF.Int
		posting_date: DF.Date
		reason_for_requesting: DF.Text | None
		requested_by: DF.Link
		requested_by_dept: DF.Link | None
		requested_by_designation: DF.Link | None
		requested_by_name: DF.Data | None
		status: DF.Literal["Pending", "Open & Approved", "Rejected", "Filled", "On Hold", "Cancelled"]
		time_to_fill: DF.Duration | None
	# end: auto-generated types

	def validate(self):
		self.validate_duplicates()
		self.set_time_to_fill()

	def validate_duplicates(self):
		duplicate = artech_engine.db.exists(
			"Job Requisition",
			{
				"designation": self.designation,
				"department": self.department,
				"requested_by": self.requested_by,
				"status": ("not in", ["Cancelled", "Filled"]),
				"name": ("!=", self.name),
			},
		)

		if duplicate:
			artech_engine.throw(
				_("A Job Requisition for {0} requested by {1} already exists: {2}").format(
					artech_engine.bold(self.designation),
					artech_engine.bold(self.requested_by),
					get_link_to_form("Job Requisition", duplicate),
				),
				title=_("Duplicate Job Requisition"),
			)

	def set_time_to_fill(self):
		if self.status == "Filled" and self.completed_on:
			self.time_to_fill = time_diff_in_seconds(self.completed_on, self.posting_date)

	@artech_engine.whitelist()
	def associate_job_opening(self, job_opening: str) -> None:
		artech_engine.db.set_value(
			"Job Opening", job_opening, {"job_requisition": self.name, "vacancies": self.no_of_positions}
		)
		artech_engine.msgprint(
			_("Job Requisition {0} has been associated with Job Opening {1}").format(
				artech_engine.bold(self.name), get_link_to_form("Job Opening", job_opening)
			),
			title=_("Job Opening Associated"),
		)


@artech_engine.whitelist()
def make_job_opening(source_name: str, target_doc: str | Document | None = None) -> Document:
	def set_missing_values(source, target):
		target.job_title = source.designation
		target.status = "Open"
		target.currency = artech_engine.db.get_value("Company", source.company, "default_currency")
		target.lower_range = source.expected_compensation
		target.description = source.description

	return get_mapped_doc(
		"Job Requisition",
		source_name,
		{
			"Job Requisition": {
				"doctype": "Job Opening",
			},
			"field_map": {
				"designation": "designation",
				"name": "job_requisition",
				"department": "department",
				"no_of_positions": "vacancies",
			},
		},
		target_doc,
		set_missing_values,
	)


@artech_engine.whitelist()
def get_avg_time_to_fill(
	company: str | None = None, department: str | None = None, designation: str | None = None
):
	filters = {"status": "Filled"}
	if company:
		filters["company"] = company
	if department:
		filters["department"] = department
	if designation:
		filters["designation"] = designation

	avg_time_to_fill = artech_engine.db.get_list(
		"Job Requisition",
		filters=filters,
		fields=[{"AVG": "time_to_fill", "as": "average_time"}],
	)[0].average_time

	return format_duration(avg_time_to_fill) if avg_time_to_fill else 0
