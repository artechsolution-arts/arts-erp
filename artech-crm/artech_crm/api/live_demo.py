# This file is used to handle live demo site (https://frappecrm-demo.artech_engine.cloud) related API calls and hooks

import artech_engine
from artech_engine import _
from artech_engine.auth import LoginManager


@artech_engine.whitelist(allow_guest=True)
def login():
	if not artech_engine.conf.demo_username or not artech_engine.conf.demo_password:
		return
	artech_engine.local.response["redirect_to"] = "/crm"
	login_manager = LoginManager()
	login_manager.authenticate(artech_engine.conf.demo_username, artech_engine.conf.demo_password)
	login_manager.post_login()
	artech_engine.local.response["type"] = "redirect"
	artech_engine.local.response["location"] = artech_engine.local.response["redirect_to"]


def validate_reset_password(doc, event):
	if artech_engine.conf.demo_username and artech_engine.session.user == artech_engine.conf.demo_username:
		artech_engine.throw(
			_("Password cannot be reset by Demo User {}").format(artech_engine.bold(artech_engine.conf.demo_username)),
			artech_engine.PermissionError,
		)


def validate_user(doc, event):
	if artech_engine.conf.demo_username and artech_engine.session.user == artech_engine.conf.demo_username and doc.new_password:
		artech_engine.throw(
			_("Password cannot be reset by Demo User {}").format(artech_engine.bold(artech_engine.conf.demo_username)),
			artech_engine.PermissionError,
		)
