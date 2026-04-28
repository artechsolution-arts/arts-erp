from contextlib import contextmanager

import artech_engine


@contextmanager
def temporary_flag(flag_name, value):
	flags = artech_engine.local.flags
	flags[flag_name] = value
	try:
		yield
	finally:
		flags.pop(flag_name, None)
