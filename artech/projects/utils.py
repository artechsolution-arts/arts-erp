# Copyright (c) 2015, Artech and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import artech_engine


@artech_engine.whitelist()
@artech_engine.validate_and_sanitize_search_inputs
def query_task(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict):
	from artech_engine.desk.reportview import build_match_conditions

	search_string = "%%%s%%" % txt
	order_by_string = "%s%%" % txt
	match_conditions = build_match_conditions("Task")
	match_conditions = (f"and ({match_conditions})") if match_conditions else ""

	return artech_engine.db.sql(
		"""select name, subject from `tabTask`
		where (`{}` like {} or `subject` like {}) {}
		order by
			case when `subject` like {} then 0 else 1 end,
			case when `{}` like {} then 0 else 1 end,
			`{}`,
			subject
		limit {} offset {}""".format(
			searchfield, "%s", "%s", match_conditions, "%s", searchfield, "%s", searchfield, "%s", "%s"
		),
		(search_string, search_string, order_by_string, order_by_string, page_len, start),
	)
