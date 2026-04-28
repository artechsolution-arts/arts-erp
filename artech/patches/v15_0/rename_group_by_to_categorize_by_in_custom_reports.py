import json

import artech_engine


def execute():
	custom_reports = artech_engine.get_all(
		"Report",
		filters={
			"report_type": "Custom Report",
			"reference_report": ["in", ["General Ledger", "Supplier Quotation Comparison"]],
		},
		fields=["name", "json"],
	)

	for report in custom_reports:
		report_json = json.loads(report.json)

		if "filters" in report_json and "group_by" in report_json["filters"]:
			report_json["filters"]["categorize_by"] = (
				report_json["filters"].pop("group_by").replace("Group", "Categorize")
			)

			artech_engine.db.set_value("Report", report.name, "json", json.dumps(report_json))
