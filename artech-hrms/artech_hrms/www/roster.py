import artech_engine


def get_context(context):
	csrf_token = artech_engine.sessions.get_csrf_token()
	artech_engine.db.commit()  # nosempgrep
	context = artech_engine._dict()
	context.csrf_token = csrf_token
	return context
