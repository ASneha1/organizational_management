# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "organizational_management"
app_title = "organizational_management"
app_publisher = "Cloude8"
app_description = "Capture the organizational hierarchy in companies and have a view on the Delegation of Authorities when transactions are being performed"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "asneha@cloude8.com"
app_version = "0.0.1"
app_license = "MIT"

doc_events = {
	"Purchase Order": {
		"validate": "organizational_management.organizational_management.doctype.purchase_order_approval_workflow.purchase_order_approval_workflow.populate_approval_workflow",
		"before_save": "organizational_management.organizational_management.doctype.purchase_order_approval_workflow.purchase_order_approval_workflow.populate_to_notify_next",
		"before_submit": "organizational_management.organizational_management.doctype.purchase_order_approval_workflow.purchase_order_approval_workflow.populate_to_notify_next"
	},
	"Expense Claim": {
		"validate": "organizational_management.organizational_management.doctype.expense_claim_approval_workflow.expense_claim_approval_workflow.populate_approval_workflow",
		"before_save": "organizational_management.organizational_management.doctype.expense_claim_approval_workflow.expense_claim_approval_workflow.populate_to_notify_next",
		"before_submit": "organizational_management.organizational_management.doctype.expense_claim_approval_workflow.expense_claim_approval_workflow.populate_to_notify_next"
	},
	"Leave Application": {
		"validate": "organizational_management.organizational_management.doctype.leave_application_approval_workflow.leave_application_approval_workflow.populate_approval_workflow",
		"before_save": "organizational_management.organizational_management.doctype.leave_application_approval_workflow.leave_application_approval_workflow.populate_to_notify_next",
		"before_submit": "organizational_management.organizational_management.doctype.leave_application_approval_workflow.leave_application_approval_workflow.populate_to_notify_next"
	},
	"Material Request": {
		"validate": "organizational_management.organizational_management.doctype.material_request_approval_workflow.material_request_approval_workflow.populate_approval_workflow",
		"before_save": "organizational_management.organizational_management.doctype.material_request_approval_workflow.material_request_approval_workflow.populate_to_notify_next",
		"before_submit": "organizational_management.organizational_management.doctype.material_request_approval_workflow.material_request_approval_workflow.populate_to_notify_next"
	}
}

notification_config = "organizational_management.notifications.get_notification_config"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/organizational_management/css/organizational_management.css"
# app_include_js = "/assets/organizational_management/js/organizational_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/organizational_management/css/organizational_management.css"
# web_include_js = "/assets/organizational_management/js/organizational_management.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "organizational_management.utils.get_home_page"

# Generators
# ----------
website_generators = ["Position"]

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "organizational_management.install.before_install"
# after_install = "organizational_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "organizational_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"organizational_management.tasks.all"
# 	],
# 	"daily": [
# 		"organizational_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"organizational_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"organizational_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"organizational_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "organizational_management.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "organizational_management.event.get_events"
# }

