import artech_engine


def execute():
	old_workspaces = ["Expense Claims", "Salary Payout", "Employee Lifecycle", "Overview", "Attendance", "HR"]

	for workspace in old_workspaces:
		if artech_engine.db.exists("Workspace", {"name": workspace, "public": 1, "for_user": ("is", "Not Set")}):
			artech_engine.delete_doc("Workspace", workspace, force=True)
		if sidebar := artech_engine.db.exists(
			"Workspace Sidebar", {"name": workspace, "for_user": ("is", "Not Set")}
		):
			artech_engine.delete_doc("Workspace Sidebar", sidebar)
		if icon := artech_engine.db.exists("Desktop Icon", {"link_type": "Workspace", "link_to": workspace}):
			artech_engine.delete_doc("Desktop Icon", icon)
