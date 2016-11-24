# -*- coding: utf-8 -*-
# Copyright (c) 2015, Cloude8 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class LeaveApplicationApprovalWorkflow(Document):
	pass

import json

@frappe.whitelist()
def populate_approval_workflow(doc, method):
	if ("Administrator" not in frappe.get_roles(frappe.session.user)):
		# If doc.status in 'Open', populate workflow. Else, check against created workflow
		if doc.status == 'Open':
			doctype = doc.doctype
			company = doc.company
			grand_total = doc.total_leave_days

			roleToUserMap = []
			roleToActionMap = []
			currUserMapped = False
			
			# Identify workflow by - Doctype, Company and is_active
			workflow_name = frappe.db.get_value("Workflow", {"document_type": doctype, "company": company, "enable_approval_workflow": 1}, "name")

			if workflow_name:
				# List of all the transitions - action(action), next_state(state), allowed(role), positive_transition(checkbox), approval_limit(Yes or No)
				transition_list = frappe.db.sql("""select action, next_state, allowed, positive_transition, approval_limit from `tabWorkflow Transition` where parent=%s""", workflow_name, as_dict=True)
				# List of all DISTINCT role that can perform transactions, in the order at workflow
				allowed_list = frappe.db.sql("""select distinct(role) from `tabWorkflow Order of Roles` where parent=%s order by order_of_role""", workflow_name, as_dict=True)

				# currUser - current user
				currUser = frappe.session.user
				# currUserPosition - position of current user (from Employee doctype via user_id)
				currUserPosition = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "position")
				# position_system_roles - roles tied to the position of the user (from Position doctype via position)
				position_system_roles = frappe.db.sql("""select `tabPosition System Role`.`role`
					from `tabPosition`, `tabPosition System Role` where `tabPosition`.`name` = %s and `tabPosition`.`name`=`tabPosition System Role`.`parent`""",
					(currUserPosition))

				index = 0
				# For each DISTINCT role, see if current user has that role in his position
				while index < len(allowed_list):
					# Traverse through roles in current user's position and if any of the role matches the DISTINCT roles that can perform transactions, append (role, user) to roleToUserMap
					for p_r in position_system_roles:
						if allowed_list[index].role == p_r[0]:
							roleUser_row = [allowed_list[index].role, frappe.session.user]
							roleToUserMap.append(roleUser_row)
							# Remove that role from the list as current user is mapped to perform that role
							allowed_list.remove(allowed_list[index])
							currUserMapped = True
							break
					else:
						# None of the DISTINCT roles are in current user's position
						# Remove that role from the list and see if user can match other remaining roles
						allowed_list.remove(allowed_list[index])
					if currUserMapped: break
				if not currUserMapped:
					frappe.throw(_("No Permission on form according to Position"))
			
				index1 = 0
				# For each DISTINCT role, see if report_to user has that role in his position
				while index1 < len(allowed_list):
					# reportTo_user - report_to_user(user) tied to the user (from Organizational Hierarchy doctype via user)
					reportTo_user = frappe.db.get_value("Organizational Hierarchy", {"user": currUser}, "report_to_user")
					# reportTo_postion - position of the reportTo_user (from Employee doctype via user_id)
					reportToPosition = frappe.db.get_value("Employee", {"user_id": reportTo_user}, "position")
					# reportTo_position_system_roles - roles tied to the position of the user (from Position doctype via position)
					reportTo_position_system_roles = frappe.db.sql("""select `tabPosition System Role`.`role`
						from `tabPosition`, `tabPosition System Role` where `tabPosition`.`name` = %s and `tabPosition`.`name`=`tabPosition System Role`.`parent`""",
						(reportToPosition))				
					# Traverse through roles in report_to_user's position and if any of the role matches the DISTINCT roles that can perform transactions, append (role, user) to roleToUserMap
					for reportTo_p_r in reportTo_position_system_roles:
						if allowed_list[index1].role == reportTo_p_r[0]:
							roleUser_row = [allowed_list[index1].role, reportTo_user]
							roleToUserMap.append(roleUser_row)
							# Remove that role from the list as reportTo_user is mapped to perform that role
							allowed_list.remove(allowed_list[index1])
							currUser = reportTo_user
							break
					else:
						# None of the DISTINCT roles are in report_to_user's position
						# Remove that role from the list and see if user can match other remaining roles
						allowed_list.remove(allowed_list[index1])
	 
				reached_approved = 0 

				# For each role in roleToUserMap(role, user), get the final_action, final_next state, possible next states(actions)
				for roleToUser in roleToUserMap:
					if reached_approved == 0:
						# action_list is in fact the possible next states list
						action_list = []
						final_action = ""
						final_next_state = ""
						for transition2 in transition_list:
							if transition2.allowed == roleToUser[0]:
								if transition2.approval_limit == "No" or is_within_approval_limit(transition2.allowed, doctype, company, grand_total):
									# if transition2.action != 'Approve' or roleToUser[1] != doc.employee_user_id:
									action = transition2.next_state
									action_list.append(action)
									if transition2.positive_transition == 1:
										final_action = transition2.action
										final_next_state = transition2.next_state
										if final_action == 'Approve':
											reached_approved = 1
						# Besides the transaction list, the other possible states the role has permission on - from Workflow Document State
						state_list = frappe.db.sql("""select state, approval_limit from `tabWorkflow Document State` where parent=%s and allow_edit=%s""", (workflow_name, roleToUser[0]), as_dict=True)
						for state1 in state_list:
							# If role has permission on state but not in transaction list, add it to state list (i.e. action_list)
							if state1.state not in action_list:
								if state1.approval_limit == "No" or is_within_approval_limit(roleToUser[0], doctype, company, grand_total):
									# if state1.state != 'Approved' or roleToUser[1] != doc.employee_user_id:
									action_list.append(state1.state)
						actions = ', '.join(action_list)
						if final_action:
							roleAction_row = [roleToUser[0], final_action, final_next_state, actions]
							roleToActionMap.append(roleAction_row)
			
				# Clear rows in approval_workflow that are still at 'Pending'
				to_remove = []
				for row1 in doc.approval_workflow:
					if row1.status == 'Pending':
						to_remove.append(row1)
				[doc.remove(row1) for row1 in to_remove]


				dictRoleToUserMap =dict(roleToUserMap) 

				# Append list to doc.approval_workflow
				for roleToAction in roleToActionMap:
					# user_position = frappe.get_value("Employee", {"user_id": dictRoleToUserMap[roleToAction[0]]}, "position")  
					# row = [roleToAction[1], roleToAction[2], dictRoleToUserMap[roleToAction[0]], user_position]   
					doc.append("approval_workflow", {"result_state": roleToAction[2], "action": roleToAction[1], "user": dictRoleToUserMap[roleToAction[0]], "status": "Pending", "possible_actions": roleToAction[3]})
			else:
				frappe.msgprint("No Enabled Approval Workflow on this form")
		else:
			isApprovalWorkflowCompleted = 1
			for d in doc.approval_workflow:
				# If status is Pending, process further, if not continue
				if d.status == 'Pending':
					isApprovalWorkflowCompleted = 0
					if frappe.session.user == d.user:
						if doc.status in d.possible_actions:
							# If thats the result_state, mark Completed, else still Pending
							if doc.status == d.result_state:
								d.status = "Completed"
								d.state = doc.status
								return
							else:
								d.status = "Pending"
								d.state = doc.status
								return
						else:
							frappe.throw(_("No Permission to perform the action"))
					else:
						frappe.throw(_("No Permission on form according to Organizational Hierarchy"))
				else:
					if frappe.session.user == d.user:
						if doc.status in d.possible_actions:
							if doc.status == d.result_state:
								d.status = "Completed"
								d.state = doc.status
								return
							else:
								d.status = "Pending"
								d.state = doc.status
								return
						else:
							frappe.throw(_("No Permission to perform the action"))

			if isApprovalWorkflowCompleted == 1:
				for d in doc.approval_workflow:
					if frappe.session.user == d.user:
						if doc.status in d.possible_actions:
							if doc.status == d.result_state:
								d.status = "Completed"
								d.state = doc.status
								return
							else:
								d.status = "Pending"
								d.state = doc.status
								return
						else:
							frappe.throw(_("No Permission to perform the action"))
				frappe.throw(_("All completed. No Permission on form according to Organizational Heirarchy"))

@frappe.whitelist()
def is_within_approval_limit(role, doctype, company, amount):
	authValue_list = frappe.db.sql("""select value from `tabApproval Limit` where company=%s and transaction=%s and role=%s""", (company, doctype, role), as_dict=True)
	if authValue_list:
		if amount > authValue_list[0].value:
			return False

	return True

@frappe.whitelist()
def populate_to_notify_next(doc, method):
	from frappe.utils.user import get_user_fullname
	approvals = doc.approval_workflow
	if len(approvals) != 0:
		for i in range(len(approvals)):
			if approvals[i].user == frappe.session.user:
				if approvals[i].status == 'Pending':
					if (i-1) >= 0:
						doc.to_notify_next = approvals[i-1].user
						return
					else:
						doc.to_notify_next = approvals[i].user
						return
				else:
				# if status is 'Completed'
					if (i+1) < len(approvals):
						doc.to_notify_next = approvals[i+1].user
						if doc.status == 'Applied':
							doc.leave_approver = approvals[i+1].user
							doc.leave_approver_name = get_user_fullname(approvals[i+1].user)
						return
					else:
						doc.to_notify_next = ''
						return