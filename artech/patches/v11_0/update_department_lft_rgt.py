import artech_engine
from artech_engine import _
from artech_engine.utils.nestedset import rebuild_tree


def execute():
	"""assign lft and rgt appropriately"""
	artech_engine.reload_doc("setup", "doctype", "department")
	if not artech_engine.db.exists("Department", _("All Departments")):
		artech_engine.get_doc(
			{"doctype": "Department", "department_name": _("All Departments"), "is_group": 1}
		).insert(ignore_permissions=True, ignore_mandatory=True)

	artech_engine.db.sql(
		"""update `tabDepartment` set parent_department = '{}'
		where is_group = 0""".format(_("All Departments"))
	)

	rebuild_tree("Department")
