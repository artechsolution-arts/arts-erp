import artech_engine

__version__ = "17.0.0-dev"


def refetch_resource(cache_key: str | list, user=None):
	artech_engine.publish_realtime(
		"hrms:refetch_resource",
		{"cache_key": cache_key},
		user=user or artech_engine.session.user,
		after_commit=True,
	)
