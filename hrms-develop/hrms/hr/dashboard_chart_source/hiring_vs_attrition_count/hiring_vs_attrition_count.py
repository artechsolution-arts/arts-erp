import artech_engine
from artech_engine import _
from artech_engine.desk.doctype.dashboard_chart.dashboard_chart import get_result
from artech_engine.utils import getdate
from artech_engine.utils.dashboard import cache_source
from artech_engine.utils.dateutils import get_period


@artech_engine.whitelist()
@cache_source
def get_data(
	chart_name: str | None = None,
	chart: str | None = None,
	no_cache: str | None = None,
	filters: str | None = None,
	from_date: str | None = None,
	to_date: str | None = None,
	timespan: str | None = None,
	time_interval: str | None = None,
	heatmap_year: str | None = None,
) -> dict[str, list]:
	if filters:
		filters = artech_engine.parse_json(filters)

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if not to_date:
		to_date = getdate()

	permitted_fields = artech_engine.model.get_permitted_fields("Employee", user=artech_engine.session.user)

	hiring = (
		get_records(from_date, to_date, "date_of_joining", filters.get("company"))
		if "date_of_joining" in permitted_fields
		else []
	)

	attrition = (
		get_records(from_date, to_date, "relieving_date", filters.get("company"))
		if "relieving_date" in permitted_fields
		else []
	)

	hiring_data = get_result(hiring, filters.get("time_interval"), from_date, to_date, "Count")
	attrition_data = get_result(attrition, filters.get("time_interval"), from_date, to_date, "Count")

	return {
		"labels": [get_period(r[0], filters.get("time_interval")) for r in hiring_data],
		"datasets": [
			{"name": _("Hiring Count"), "values": [r[1] for r in hiring_data]},
			{"name": _("Attrition Count"), "values": [r[1] for r in attrition_data]},
		],
	}


def get_records(from_date: str, to_date: str, datefield: str, company: str) -> tuple[tuple[str, float, int]]:
	filters = [
		["Employee", "company", "=", company],
		["Employee", datefield, ">=", from_date],
		["Employee", datefield, "<=", to_date],
	]

	data = artech_engine.db.get_list(
		"Employee",
		fields=[f"{datefield} as _unit", {"SUM": 1}, {"COUNT": "*"}],
		filters=filters,
		group_by="_unit",
		order_by="_unit asc",
		as_list=True,
		ignore_ifnull=True,
	)

	return data
