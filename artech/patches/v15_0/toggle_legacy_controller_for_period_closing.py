import artech_engine


def execute():
	"""
	Description:
	Enable Legacy controller for Period Closing Voucher
	"""
	artech_engine.db.set_single_value("Accounts Settings", "use_legacy_controller_for_pcv", 1)
