// Copyright (c) 2016, Cloude8 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Organizational Hierarchy', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on("Organizational Hierarchy", "user", function(frm) {
    frappe.call({
        "method": "frappe.client.get_value",
        "args": {
            "doctype": "Employee",
            "fieldname": "position",
            "filters": {
                "user_id":  cur_frm.doc.user
            }
        },
        callback: function(r){
			frappe.call({
			"method": "frappe.client.get_value",
			"args": {
				"doctype": "Position",
				"fieldname": "report_to",
				"filters": {
					"name":  r.message.position
				}
			},
			callback: function(r){
				 frappe.call({
					"method": "frappe.client.get_value",
					"args": {
						"doctype": "Employee",
						"fieldname": "user_id",
						"filters": {
							"position":  r.message.report_to
						}
					},
					callback: function(r){
						 console.log(r.message.user_id);
						 cur_frm.set_value("report_to_user", r.message.user_id);
					}
					})
			}
			})
       }
    })
});