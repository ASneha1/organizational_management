from __future__ import unicode_literals
import frappe

def get_notification_config():
	return {
		"for_doctype": {
			"Purchase Order": {"to_notify_next": frappe.session.user},
			"Expense Claim": {"approval_status": "Applied", "to_notify_next": frappe.session.user},
			"Leave Application": {"status": "Applied", "to_notify_next": frappe.session.user},
		}
	}