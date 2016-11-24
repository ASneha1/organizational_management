from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1
no_sitemap = 1

@frappe.whitelist(allow_guest=False)
def get_context(context):
    #frappe.throw(_(str(context)))

    #if not context.doc.has_website_permission("read"):
    #	frappe.throw(_("Not Permitted"), frappe.PermissionError)
    #	return
    context.all = get_chart()
    context.all_name = get_name()
    context.sort_name = get_sort_name()


@frappe.whitelist(allow_guest=False)
def get_chart(**kwargs):
    position_list =  frappe.get_list("Position",fields=["*"],filters = [["is_active","=","Yes"]], order_by="department desc", **kwargs)
    not_head_list =  frappe.get_list("Position",fields=["*"],filters = [["is_active","=","Yes"],["head","=","0"]], order_by="department desc", **kwargs)
	
    validation (not_head_list)
    chart = list()
    chart = arrange_positions(position_list)
    add_data(chart)
    return chart


def get_name():
	check = frappe.get_list("Position",fields=["*"],filters = [["is_active","=","Yes"]])
	name_list = frappe.get_list("Employee",fields=["*"], order_by="employee_name ")
	name = []

	for x in name_list:
		for y in check:
			if x.employee_position == y.page_name:
				name.append(x)
				break

	return name


def get_sort_name():
 	position_list =  frappe.get_list("Position",fields=["*"],filters = [["is_active","=","Yes"]], order_by="page_name")
	return position_list


	
def validation(positions):
	for position in positions:
		if position.report_to == "board of director":
			frappe.throw(_("{0} report to board of director ").format(position.page_name))

		elif position.report_to == position.page_name:
			frappe.throw(_("{0} report to itself ").format(position.page_name))

		if position.page_name == "board of director":
			break
		count =0

		position_list =  frappe.get_list("Position",fields=["*"],filters = [["is_active","=","Yes"],["board","=","0"]], order_by="department desc")
		for x in position_list:
			if position.report_to == x.page_name:
				count = count + 1
		
		if count == 0:
			frappe.throw(_("{0} report to non-existing position ").format(position.page_name))

	





def add_data(chart, **kwargs):
    employee_list =  frappe.get_list("Employee",fields=["*"], **kwargs)
    for employee in employee_list:
        if employee.employee_position != None:
            tag_position(employee, chart)

def tag_position(employee, chart, **kwargs):
    pointer = employee.position

    employee_list =  frappe.get_list("Employee",fields=["*"],filters = [["naming_series","=",employee]], **kwargs)
    employee = employee_list.pop()
    word = str(employee)
    word_array = word.split(",")
    return_word = ""

    for x in range (0, len(word_array)):
        variable = word_array[x]
        variable_array = variable.split(":")

        if variable_array[0] == "bio":
            clean_data(1, variable)

        elif  len(variable_array) > 1:
            return_input1 = str(x) + "^"+ clean_data(2, variable_array[1])
        else:
            # return_input1 = "[V0]" + variable_array[0]
            return_input1 = "None0,"

        return_input2 = return_input1
        return_word = return_word + return_input2 + ","


    for position in chart:
        if position.page_name == pointer:
            position.others_website = return_word
            return


def clean_data(fun, data):
    data = data[3:-1] 
    
    if (fun == 1):
        data = "Bio,"

    elif "<p" in data:
        data = "clear p,"

    return data


@frappe.whitelist(allow_guest=False)
def arrange_positions(positions):
    chart = []
    first_position = get_first_position(positions)
    #frappe.throw(_(str(first_position)))

    if first_position is None:
        return first_position

    chart.append(first_position)

    #frappe.throw(_(str(positions)))
    positions.remove(first_position)
    
    reporting_chart = []

    report_to = first_position.page_name
    reporting_chart.append(report_to)

    loop_num = 0
    loop_once = False
  
    level = 2
    list_num = 1
    
    #Loop till all position pushed Chart list
    while (len(positions) > 0):
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
        for position in positions:
	    if report_to == position.report_to:
                position.level = level
                position.list_num = list_num
                chart.append(position)
                positions.remove(position)
                report_to = position.page_name
                reporting_chart.append(report_to)
                loop_num = 0
                level = level + 1
                list_num = list_num + 1
            
            if len(positions) == 0:
                break
    
    return chart


@frappe.whitelist(allow_guest=False)
def get_first_position(positions):
    for position in positions:
        if position.board == 1.:
            position.level = 1
            position.list_num = 0
            return position

    return positions


@frappe.whitelist()
def get_employee_data(id):
    testing_text = 'Testing'
    return testing_text