app_name = "artech_crm"
app_title = "Artech CRM"
app_publisher = "Artech Solutions"
app_description = "Kick-ass Open Source CRM"
app_email = "artechnical707@gmail.com"
app_license = "AGPLv3"
app_icon_url = "/assets/artech_crm/images/logo.svg"
app_icon_title = "CRM"
app_icon_route = "/artech_crm"

# Apps
# ------------------

# required_apps = []
add_to_apps_screen = [
	{
		"name": "artech_crm",
		"logo": "/assets/artech_crm/images/logo.svg",
		"title": "CRM",
		"route": "/artech_crm",
		"has_permission": "artech_crm.api.check_app_permission",
	}
]

get_site_info = "artech_crm.activation.get_site_info"

export_python_type_annotations = True
require_type_annotated_api_methods = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/artech_crm/css/artech_crm.css"
# app_include_js = "/assets/artech_crm/js/artech_crm.js"

# include js, css files in header of web template
# web_include_css = "/assets/artech_crm/css/artech_crm.css"
# web_include_js = "/assets/artech_crm/js/artech_crm.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "artech_crm/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

website_route_rules = [
	{"from_route": "/artech_crm/<path:app_path>", "to_route": "artech_crm"},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# "methods": "artech_crm.utils.jinja_methods",
# "filters": "artech_crm.utils.jinja_filters"
# }

# Setup wizard
# setup_wizard_requires = "assets/artech_crm/js/setup_wizard.js"
# setup_wizard_stages = "artech_crm.setup.setup_wizard.setup_wizard.get_setup_stages"
setup_wizard_complete = "artech_crm.demo.api.create_demo_data"
# setup_wizard_test = "artech_crm.setup.setup_wizard.test_setup_wizard.run_setup_wizard_test"

# Installation
# ------------

before_install = "artech_crm.install.before_install"
after_install = "artech_crm.install.after_install"

# Uninstallation
# ------------

before_uninstall = "artech_crm.uninstall.before_uninstall"
# after_uninstall = "artech_crm.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "artech_crm.utils.before_app_install"
# after_app_install = "artech_crm.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "artech_crm.utils.before_app_uninstall"
# after_app_uninstall = "artech_crm.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See artech_engine.core.notifications.get_notification_config

# notification_config = "artech_crm.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# "Event": "artech_engine.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# "Event": "artech_engine.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Contact": "artech_crm.overrides.contact.CustomContact",
	"Email Template": "artech_crm.overrides.email_template.CustomEmailTemplate",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Contact": {
		"validate": ["artech_crm.api.contact.validate"],
	},
	"ToDo": {
		"after_insert": ["artech_crm.api.todo.after_insert"],
		"on_update": ["artech_crm.api.todo.on_update"],
	},
	"Communication": {
		"after_insert": ["artech_crm.utils.on_communication_insert"],
		"on_update": ["artech_crm.utils.on_communication_update"],
	},
	"Comment": {
		"after_insert": ["artech_crm.utils.on_comment_insert"],
		"on_update": ["artech_crm.api.comment.on_update"],
	},
	"WhatsApp Message": {
		"validate": ["artech_crm.api.whatsapp.validate"],
		"on_update": ["artech_crm.api.whatsapp.on_update"],
	},
	"CRM Deal": {
		"on_update": [
			"artech_crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings.create_customer_in_erpnext"
		],
	},
	"User": {
		"before_validate": ["artech_crm.api.live_demo.validate_user"],
		"validate_reset_password": ["artech_crm.api.live_demo.validate_reset_password"],
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": ["artech_crm.api.event.trigger_offset_event_notifications"],
	"hourly": ["artech_crm.api.event.trigger_hourly_event_notifications"],
	"daily": ["artech_crm.api.event.trigger_daily_event_notifications"],
	"weekly": ["artech_crm.api.event.trigger_weekly_event_notifications"],
	"daily_long": ["artech_crm.lead_syncing.background_sync.sync_leads_from_sources_daily"],
	"hourly_long": ["artech_crm.lead_syncing.background_sync.sync_leads_from_sources_hourly"],
	"monthly_long": ["artech_crm.lead_syncing.background_sync.sync_leads_from_sources_monthly"],
	"cron": {
		"*/5 * * * *": ["artech_crm.lead_syncing.background_sync.sync_leads_from_sources_5_minutes"],
		"*/10 * * * *": ["artech_crm.lead_syncing.background_sync.sync_leads_from_sources_10_minutes"],
		"*/15 * * * *": ["artech_crm.lead_syncing.background_sync.sync_leads_from_sources_15_minutes"],
	},
}

# Testing
# -------

before_tests = "artech_crm.tests.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# "artech_engine.desk.doctype.event.event.get_events": "artech_crm.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# "Task": "artech_crm.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

ignore_links_on_delete = ["Failed Lead Sync Log"]

# Request Events
# ----------------
# before_request = ["artech_crm.utils.before_request"]
# after_request = ["artech_crm.utils.after_request"]

# Job Events
# ----------
# before_job = ["artech_crm.utils.before_job"]
# after_job = ["artech_crm.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# {
# "doctype": "{doctype_1}",
# "filter_by": "{filter_by}",
# "redact_fields": ["{field_1}", "{field_2}"],
# "partial": 1,
# },
# {
# "doctype": "{doctype_2}",
# "filter_by": "{filter_by}",
# "partial": 1,
# },
# {
# "doctype": "{doctype_3}",
# "strict": False,
# },
# {
# "doctype": "{doctype_4}"
# }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# "artech_crm.auth.validate"
# ]

after_migrate = [
	"artech_crm.fcrm.doctype.fcrm_settings.fcrm_settings.after_migrate",
	"artech_crm.api.whatsapp.add_roles",
]

standard_dropdown_items = [
	{
		"name1": "app_selector",
		"label": "Apps",
		"type": "Route",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "settings",
		"label": "Settings",
		"type": "Route",
		"icon": "settings",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "login_to_fc",
		"label": "Login to Frappe Cloud",
		"type": "Route",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "about",
		"label": "About",
		"type": "Route",
		"icon": "info",
		"route": "#",
		"is_standard": 1,
	},
	{
		"name1": "separator",
		"label": "",
		"type": "Separator",
		"is_standard": 1,
	},
	{
		"name1": "logout",
		"label": "Log out",
		"type": "Route",
		"icon": "log-out",
		"route": "#",
		"is_standard": 1,
	},
]
