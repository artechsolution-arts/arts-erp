import artech_engine
from artech_engine.model.utils.rename_field import rename_field


def execute():
	try:
		if artech_engine.db.has_column("Employee Benefit Claim", "claim_date"):
			rename_field("Employee Benefit Claim", "claim_date", "payroll_date")

	except Exception as e:
		if e.args[0] != 1054:
			raise
