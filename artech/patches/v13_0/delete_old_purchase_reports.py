# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import artech_engine

from artech.accounts.utils import check_and_delete_linked_reports


def execute():
	reports_to_delete = [
		"Requested Items To Be Ordered",
		"Purchase Order Items To Be Received or Billed",
		"Purchase Order Items To Be Received",
		"Purchase Order Items To Be Billed",
	]

	for report in reports_to_delete:
		if artech_engine.db.exists("Report", report):
			delete_links_from_desktop_icons(report)
			delete_auto_email_reports(report)
			check_and_delete_linked_reports(report)

			artech_engine.delete_doc("Report", report, force=True)


def delete_auto_email_reports(report):
	"""Check for one or multiple Auto Email Reports and delete"""
	auto_email_reports = artech_engine.db.get_values("Auto Email Report", {"report": report}, ["name"])
	for auto_email_report in auto_email_reports:
		artech_engine.delete_doc("Auto Email Report", auto_email_report[0])


def delete_links_from_desktop_icons(report):
	"""Check for one or multiple Desktop Icons and delete"""
	desktop_icons = artech_engine.db.get_values("Desktop Icon", {"_report": report}, ["name"])
	for desktop_icon in desktop_icons:
		artech_engine.delete_doc("Desktop Icon", desktop_icon[0], force=True)
