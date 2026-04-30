import artech_engine
from artech_engine import _
from artech_engine.model.document import Document
from artech_engine.query_builder.functions import Avg
from artech_engine.utils import flt, get_link_to_form, now

from artech_hrms.hr.doctype.appraisal_cycle.appraisal_cycle import validate_active_appraisal_cycle
from artech_hrms.hr.utils import validate_active_employee
from artech_hrms.mixins.appraisal import AppraisalMixin
from artech_hrms.payroll.utils import sanitize_expression


class Appraisal(Document, AppraisalMixin):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		from artech_hrms.hr.doctype.appraisal_goal.appraisal_goal import AppraisalGoal
		from artech_hrms.hr.doctype.appraisal_kra.appraisal_kra import AppraisalKRA
		from artech_hrms.hr.doctype.employee_feedback_rating.employee_feedback_rating import EmployeeFeedbackRating

		amended_from: DF.Link | None
		appraisal_cycle: DF.Link
		appraisal_kra: DF.Table[AppraisalKRA]
		appraisal_template: DF.Link | None
		avg_feedback_score: DF.Float
		company: DF.Link
		department: DF.Link | None
		designation: DF.Link | None
		employee: DF.Link
		employee_image: DF.AttachImage | None
		employee_name: DF.Data | None
		end_date: DF.Date | None
		final_score: DF.Float
		goal_score_percentage: DF.Float
		goals: DF.Table[AppraisalGoal]
		naming_series: DF.Literal["HR-APR-.YYYY.-"]
		rate_goals_manually: DF.Check
		reflections: DF.TextEditor | None
		remarks: DF.Text | None
		self_ratings: DF.Table[EmployeeFeedbackRating]
		self_score: DF.Float
		start_date: DF.Date | None
		total_score: DF.Float
	# end: auto-generated types

	def validate(self):
		self.set_kra_evaluation_method()

		validate_active_employee(self.employee)
		validate_active_appraisal_cycle(self.appraisal_cycle)
		self.validate_duplicate()
		self.validate_total_weightage("appraisal_kra", "KRAs")
		self.validate_total_weightage("self_ratings", "Self Ratings")

		self.set_goal_score()
		self.calculate_self_appraisal_score()
		self.calculate_avg_feedback_score()
		self.calculate_final_score()

	def validate_duplicate(self):
		Appraisal = artech_engine.qb.DocType("Appraisal")
		duplicate = (
			artech_engine.qb.from_(Appraisal)
			.select(Appraisal.name)
			.where(
				(Appraisal.employee == self.employee)
				& (Appraisal.docstatus != 2)
				& (Appraisal.name != self.name)
				& (
					(Appraisal.appraisal_cycle == self.appraisal_cycle)
					| (
						(Appraisal.start_date.between(self.start_date, self.end_date))
						| (Appraisal.end_date.between(self.start_date, self.end_date))
						| (
							(self.start_date >= Appraisal.start_date)
							& (self.start_date <= Appraisal.end_date)
						)
						| ((self.end_date >= Appraisal.start_date) & (self.end_date <= Appraisal.end_date))
					)
				)
			)
		).run()
		duplicate = duplicate[0][0] if duplicate else 0

		if duplicate:
			artech_engine.throw(
				_(
					"Appraisal {0} already exists for Employee {1} for this Appraisal Cycle or overlapping period"
				).format(get_link_to_form("Appraisal", duplicate), artech_engine.bold(self.employee_name)),
				exc=artech_engine.DuplicateEntryError,
				title=_("Duplicate Entry"),
			)

	def set_kra_evaluation_method(self):
		if (
			self.is_new()
			and self.appraisal_cycle
			and (
				artech_engine.db.get_value("Appraisal Cycle", self.appraisal_cycle, "kra_evaluation_method")
				== "Manual Rating"
			)
		):
			self.rate_goals_manually = 1

	@artech_engine.whitelist()
	def set_appraisal_template(self):
		"""Sets appraisal template from Appraisee table in Cycle"""
		if not self.appraisal_cycle:
			return

		appraisal_template = artech_engine.db.get_value(
			"Appraisee",
			{
				"employee": self.employee,
				"parent": self.appraisal_cycle,
			},
			"appraisal_template",
		)

		if appraisal_template:
			self.appraisal_template = appraisal_template
			self.set_kras_and_rating_criteria()

	@artech_engine.whitelist()
	def set_kras_and_rating_criteria(self):
		if not self.appraisal_template:
			return

		self.set("appraisal_kra", [])
		self.set("self_ratings", [])
		self.set("goals", [])

		template = artech_engine.get_doc("Appraisal Template", self.appraisal_template)

		for entry in template.goals:
			table_name = "goals" if self.rate_goals_manually else "appraisal_kra"

			self.append(
				table_name,
				{
					"kra": entry.key_result_area,
					"per_weightage": entry.per_weightage,
				},
			)

		for entry in template.rating_criteria:
			self.append(
				"self_ratings",
				{
					"criteria": entry.criteria,
					"per_weightage": entry.per_weightage,
				},
			)

		return self

	def calculate_total_score(self):
		total_weightage, total, goal_score_percentage = 0, 0, 0
		meta = artech_engine.get_meta("Appraisal Goal")
		number_of_stars = meta.get_options("score") or 5
		if self.rate_goals_manually:
			table = _("Goals")
			for entry in self.goals:
				if flt(entry.score) > flt(number_of_stars):
					artech_engine.throw(
						_("Row {0}: Goal Score cannot be greater than {1}").format(entry.idx, number_of_stars)
					)

				entry.score_earned = flt(entry.score) * flt(entry.per_weightage) / 100
				total += flt(entry.score_earned)
				total_weightage += flt(entry.per_weightage)

		else:
			table = _("KRAs")
			for entry in self.appraisal_kra:
				goal_score_percentage += flt(entry.goal_score)
				total_weightage += flt(entry.per_weightage)

			self.goal_score_percentage = flt(goal_score_percentage, self.precision("goal_score_percentage"))
			# convert goal score percentage to total score out of 5
			total = flt(goal_score_percentage) / 20

		if total_weightage and flt(total_weightage, 2) != 100.0:
			artech_engine.throw(
				_("Total weightage for all {0} must add up to 100. Currently, it is {1}%").format(
					table, total_weightage
				),
				title=_("Incorrect Weightage Allocation"),
			)

		self.total_score = flt(total, self.precision("total_score"))

	def calculate_self_appraisal_score(self):
		total = 0
		meta = artech_engine.get_meta("Employee Feedback Rating")
		number_of_stars = meta.get_options("rating") or 5
		for entry in self.self_ratings:
			score = flt(entry.rating) * flt(number_of_stars) * flt(entry.per_weightage / 100)
			total += flt(score)

		self.self_score = flt(total, self.precision("self_score"))

	def calculate_avg_feedback_score(self, update=False):
		avg_feedback_score = artech_engine.qb.avg(
			"Employee Performance Feedback",
			"total_score",
			{"employee": self.employee, "appraisal": self.name, "docstatus": 1},
		)

		self.avg_feedback_score = flt(avg_feedback_score, self.precision("avg_feedback_score"))

		if update:
			self.calculate_final_score()
			self.db_update()

	def calculate_final_score(self):
		final_score = 0
		appraisal_cycle_doc = artech_engine.get_cached_doc("Appraisal Cycle", self.appraisal_cycle)

		formula = appraisal_cycle_doc.final_score_formula
		based_on_formula = appraisal_cycle_doc.calculate_final_score_based_on_formula

		if based_on_formula:
			employee_doc = artech_engine.get_cached_doc("Employee", self.employee)
			data = {
				"goal_score": flt(self.total_score),
				"average_feedback_score": flt(self.avg_feedback_score),
				"self_appraisal_score": flt(self.self_score),
			}
			data.update(appraisal_cycle_doc.as_dict())
			data.update(employee_doc.as_dict())
			data.update(self.as_dict())

			sanitized_formula = sanitize_expression(formula)
			final_score = artech_engine.safe_eval(sanitized_formula, data)
		else:
			final_score = (flt(self.total_score) + flt(self.avg_feedback_score) + flt(self.self_score)) / 3

		self.final_score = flt(final_score, self.precision("final_score"))

	@artech_engine.whitelist()
	def add_feedback(self, feedback: str, feedback_ratings: list) -> Document:
		feedback = artech_engine.get_doc(
			{
				"doctype": "Employee Performance Feedback",
				"appraisal": self.name,
				"employee": self.employee,
				"added_on": now(),
				"feedback": feedback,
				"reviewer": artech_engine.db.get_value("Employee", {"user_id": artech_engine.session.user}),
			}
		)

		for entry in feedback_ratings:
			feedback.append(
				"feedback_ratings",
				{
					"criteria": entry.get("criteria"),
					"rating": entry.get("rating"),
					"per_weightage": entry.get("per_weightage"),
				},
			)

		feedback.submit()

		return feedback

	def set_goal_score(self, update=False):
		for kra in self.appraisal_kra:
			# update progress for all goals as KRA linked could be removed or changed
			Goal = artech_engine.qb.DocType("Goal")
			avg_goal_completion = (
				artech_engine.qb.from_(Goal)
				.select(Avg(Goal.progress).as_("avg_goal_completion"))
				.where(
					(Goal.kra == kra.kra)
					& (Goal.employee == self.employee)
					# archived goals should not contribute to progress
					& (Goal.status != "Archived")
					& ((Goal.parent_goal == "") | (Goal.parent_goal.isnull()))
					& (Goal.appraisal_cycle == self.appraisal_cycle)
				)
			).run()[0][0]

			kra.goal_completion = flt(avg_goal_completion, kra.precision("goal_completion"))
			kra.goal_score = flt(kra.goal_completion * kra.per_weightage / 100, kra.precision("goal_score"))

			if update:
				kra.db_update()

		self.calculate_total_score()

		if update:
			self.calculate_final_score()
			self.db_update()

		return self


@artech_engine.whitelist()
def get_feedback_history(employee: str, appraisal: str) -> dict:
	data = artech_engine._dict()
	data.feedback_history = artech_engine.get_list(
		"Employee Performance Feedback",
		filters={"employee": employee, "appraisal": appraisal, "docstatus": 1},
		fields=[
			"feedback",
			"reviewer",
			"user",
			"owner",
			"reviewer_name",
			"reviewer_designation",
			"added_on",
			"employee",
			"total_score",
			"name",
		],
		order_by="added_on desc",
	)

	# get percentage of reviews per rating
	reviews_per_rating = []

	feedback_count = artech_engine.db.count(
		"Employee Performance Feedback",
		filters={
			"appraisal": appraisal,
			"employee": employee,
			"docstatus": 1,
		},
	)

	for i in range(1, 6):
		count = artech_engine.db.count(
			"Employee Performance Feedback",
			filters={
				"appraisal": appraisal,
				"employee": employee,
				"total_score": ("between", [i, i + 0.99]),
				"docstatus": 1,
			},
		)

		percent = flt((count / feedback_count) * 100, 0) if feedback_count else 0
		reviews_per_rating.append(percent)

	data.reviews_per_rating = reviews_per_rating
	data.avg_feedback_score = artech_engine.db.get_value("Appraisal", appraisal, "avg_feedback_score")

	return data


@artech_engine.whitelist()
@artech_engine.validate_and_sanitize_search_inputs
def get_kras_for_employee(
	doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict
) -> tuple[tuple[str]]:
	appraisal = artech_engine.db.get_value(
		"Appraisal",
		{
			"appraisal_cycle": filters.get("appraisal_cycle"),
			"employee": filters.get("employee"),
		},
		"name",
	)

	return artech_engine.get_all(
		"Appraisal KRA",
		filters={"parent": appraisal, "kra": ("like", f"{txt}%")},
		fields=["kra"],
		as_list=1,
	)
