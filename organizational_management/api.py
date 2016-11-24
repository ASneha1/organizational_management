from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.defaults
from frappe.model.document import Document
import json
from frappe.website.website_generator import WebsiteGenerator

@frappe.whitelist()
def tag_employee(position_1, doc):
    position_tagged = position_1
    position_list =  call_position(position_1)
    for position in position_list:
        if position != None:
            position.employee_tagged = doc

    

def call_position(position_1, **kwargs):
    position_list =  frappe.get_list("Position",fields=["*"],filters = [["page_name", "=", position_1]], **kwargs)
    if position_list is None:
        frappe.msgprint("None")
    return position_list



@frappe.whitelist()
def get_employee(id, value):
    value =  get_employee_list(value)

    if value == None:
        return -1
    else:
        return value

def get_employee_list(value, **kwargs):
    employee_id = clean_value(value)
    employee_list =  frappe.get_list("Employee",fields=["*"],**kwargs)
    position_list = frappe.get_list("Position",fields=["*"], **kwargs)
    position = None


    for position1 in position_list:
        if position1.page_name == employee_id:
            position = position1
            break


    for employee in employee_list:
        if employee.employee_position == position.page_name:
            return employee

    return None

def clean_value(value):
    value_list = value.split(",")
    return value_list[0]

@frappe.whitelist()
def search_employee(search_name, search_position):
    final_employee = None
    final_employee_position = None
    final_position = None

    if search_name != None:
        employee_list =  get_employee_lists()
        for employee in employee_list:
            if employee.employee_name == search_name:
                if employee.employee_position!= None:
                    final_employee =  employee


    if final_employee != None:
        position_list = get_position_lists()
        for position in position_list:
            if final_employee.employee_position== position.page_name:
                final_employee_position = position

    if search_position != "-1":
        position_list = get_position_lists()
        for position in position_list:
            if search_position == position.page_name:
                final_position = position

    if final_employee_position == None and final_position == None and final_employee == None:
        frappe.msgprint("Position cannot been found")
        return "None"

    elif final_employee_position != None and final_position != None and final_employee_position.page_name != final_position.page_name:
        frappe.msgprint("Two Positions found. Reinput search fields again")
        return "None"
    
    elif final_employee_position != None:
        return final_employee_position

    elif final_position != None:
        return final_position

    frappe.msgprint("Position cannot been found. Contact Admin.")

@frappe.whitelist()
def get_arranged_search(position2):
    position_compare = None
    position_list = get_position_lists()
    return_list = []
    remove = -1

    for position1 in position_list:
        if position1.page_name == position2:
            position_compare = position1

    report_to = position_compare.report_to
    while (remove < 5):
        for position in position_list:
            if position.page_name == report_to:
                report_to = position.report_to
                position.level = -1
                return_list.insert(0,position)
                remove = remove - 1

        remove = remove + 1

    remove = 0
    
    child_list = []
    position_compare.level = 0
    child_list.append(position_compare)
    return_list.append(position_compare)
    report_to = position_compare.page_name

    for position in return_list:
        position_list.remove(position)

    position_list1 = list(position_list)
    count = 0
    level = 1
    fixed_level = level
    push_back = "True"
    report_to_position = None



    while (remove < 10):
        for position in position_list:
            if position.report_to == report_to:
                report_to = position.page_name
                child_list.append(position)
                return_list.append(position)

                if report_to_position != None:
                    position.level = report_to_position.level + 1
                    report_to_position = position
                else:
                    report_to_position = position
                    position.level = level

                level = level + 1

                position_list1.remove(position)
                
                remove = 0
                break

        remove = remove + 1
        position_list = list (position_list1)

        if len(child_list) > 0 and remove > 5:
            remove = 0
            temp = child_list.pop()
            report_to = temp.page_name


            if push_back == "True":
                push_back = "False"
                child_list.append(temp)
                report_to_position = temp
            else:
                push_back = "True"




            if fixed_level == level:
                level = level 
            else: 
                level = level - 1 
                fixed_level = level

        


    
# while (remove < 10):
#         for position in position_list:
#             if position.report_to == report_to:
#                 report_to = position.page_name
#                 return_list.append(position)
#                 position.level = level
#                 level = level + 1
#                 position_list1.remove(position)
#                 child_list.append(position)
#                 remove = 0
#                 break

#         remove = remove + 1
#         position_list = list (position_list1)

#         if len(child_list) > 0 and remove > 5:
#             remove = 0
#             temp = child_list.pop()
#             report_to = temp.page_name
#             if fixed_level == level:
#                 level = level 
#             else: 
#                 level = level - 1 
#                 fixed_level = level



    
        


    return return_list



def get_employee_lists(**kwargs):
    return frappe.get_list("Employee",fields=["*"],**kwargs)


def get_position_lists(**kwargs):
    return frappe.get_list("Position",fields=["*"],filters = [["is_active","=","Yes"]],**kwargs)


@frappe.whitelist(allow_guest=False)
def get_required_search(position2):
    position_compare = None
    position_list = get_position_lists()
    return_list = []
    remove = -1

    for position1 in position_list:
        if position1.page_name == position2:
            position_compare = position1

    report_to = position_compare.report_to

    while (remove < 5):
        for position in position_list:
            if position.page_name == report_to:
                report_to = position.report_to
                position.level = -1
                return_list.insert(0,position)
                remove = remove - 1

        remove = remove + 1

    remove = 0
    
    child_list = []
    child_list.append(position_compare)
    return_list.append(position_compare)
    report_to = position_compare.page_name

    for position in return_list:
        position_list.remove(position)

    position_list1 = list(position_list)
    count = 0
    push_back = "True"
    report_to_position = None



    while (remove < 10):
        for position in position_list:
            if position.report_to == report_to:
                report_to = position.page_name
                child_list.append(position)
                return_list.append(position)

                if report_to_position != None:
                    report_to_position = position
                else:
                    report_to_position = position


                position_list1.remove(position)
                
                remove = 0
                break

        remove = remove + 1
        position_list = list (position_list1)

        if len(child_list) > 0 and remove > 5:
            remove = 0
            temp = child_list.pop()
            report_to = temp.page_name


            if push_back == "True":
                push_back = "False"
                child_list.append(temp)
                report_to_position = temp
            else:
                push_back = "True"
#start of something

    chart = []
    first_position = return_list.pop(0)

    if first_position is None:
        return first_position

    chart.append(first_position)
    
    reporting_chart = []
    
    report_to = first_position.page_name
    reporting_chart.append(report_to)
    loop_num = 0
    loop_once = False

    level = 2
    list_num = 1
    
    # #Loop till all position pushed Chart list
    while (len(return_list) > 0):
        loop_num = loop_num + 1
        if loop_num > 2 and len(reporting_chart) > 0:
            report_to = reporting_chart.pop()
            loop_num = 0
            
            if loop_once is False:
                reporting_chart.append(report_to)
                loop_once = True
                
            else:
                loop_once = False
                level = level - 1
                
        #Loop all position to chart on the condition that they are one branch below report_to
        for position in return_list:
            if report_to == position.report_to:
                position.level = level
                position.list_num = list_num
                chart.append(position)
                return_list.remove(position)
                report_to = position.page_name
                reporting_chart.append(report_to)
                loop_num = 0
                level = level + 1
                list_num = list_num + 1
            
            if len(return_list) == 0:
                break
    
    return chart





