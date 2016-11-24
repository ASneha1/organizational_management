// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Position', {
	refresh: function(frm) {
        // use the __islocal value of doc, to check if the doc is saved or not
        frm.set_df_property("title", "read_only", frm.doc.__islocal ? 0 : 1);
	}
});

frappe.ui.form.on("Position", "designation", function(frm){
    var position_name = frm.doc.designation + ", " + frm.doc.department
    cur_frm.set_value("title", position_name);
})

frappe.ui.form.on("Position", "department", function(frm){
    var position_name = frm.doc.designation + ", " + frm.doc.department
    cur_frm.set_value("title", position_name);
})

frappe.ui.form.on("Position", "refresh", function(frm) {
    cur_frm.set_query("report", function() {
        return {
            filters: [
                ['Position','page_name','!=','board of director']

            ]
        };
    });
});

frappe.ui.form.on("Position", "refresh", function(frm) {
    frm.add_custom_button(__("Export"), function() {
		var doctype = cur_frm.doc;
		frappe.call({
			method : "organizational_management.organizational_management.doctype.position.position.get_template",
			args: {
				doctype: doctype,
				parent_doctype: doctype,
				with_data: yes
			}
		})
			


    });
});

frappe.ui.form.on("Position", "refresh", function(frm) {
    frm.add_custom_button(__("Navigate to Org Chart"), function() {

		window.location.href = "http://"+window.location.hostname+"/chart";

     
     });
});

