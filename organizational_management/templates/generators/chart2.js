function mouseOver(id, value1) {
    frappe.call({
        method: "organizational_management.api.get_employee",
        args: {
            id: id,
            value: document.getElementById(id).getAttribute("value")
        },
        callback: function(r) {
            document.getElementById("position_data").style = "float: middle;";

            var static_info = "<h3>Position Information</h3>";
            var position = document.getElementById(id).getAttribute("value");
            var details = position.split(",");
            var page_name = "<b>ID: </b>" + details[0] + "<br>"; 
            var company = "<b>Company: </b>" + details[1] + "<br>"; 
            var department = "<b>Department: </b>" + details[2] + "<br>"; 
            var designation = "<b>Designation: </b>" + details[3] + "<br>"; 
            var job_description = "<b>Job Description: </b>" + details[4] + "<br>"; 
            var position_band = "<b>Position Band: </b>" + details[5] + "<br>"; 
            var report_to = "<b>Report To: </b>" + details[6] + "<br>"; 

            var position_data_display = static_info + page_name + company + department + designation + job_description + position_band + report_to;
            document.getElementById("position_data").innerHTML = position_data_display;

            var employee_data_display = "";
            var employee_data = r.message;

            if (employee_data == -1){
                employee_data_display = "<i>No Employee tagged to this position</i>";

            } else {
                var image = "<img src ='" + employee_data.image + "'><br>"; 
                var employee_id = "<b>ID: </b>" + employee_data.employee + "<br>"; 
                var name = "<b>Name: </b>" + employee_data.salutation + " " + employee_data.employee_name + "<br>"; 
                var username = "<b>Username: </b>" + employee_data.user_id + "<br>"; 
                var date_joined = "<b>Date Joined: </b>" + employee_data.date_of_joining + "<br>"; 
                var dob = "<b>Date of Birth: </b>" + employee_data.date_of_birth + "<br>"; 
                var gender = "<b>Gender: </b>" + employee_data.gender + "<br>"; 
                var status = "<b>Status: </b>" + employee_data.employee + "<br>"; 
                var employment_type = "<b>Employment Type: </b>" + employee_data.employment_type + "<br>"; 
                var offer_date = "<b>Offer Date: </b>" + employee_data.scheduled_confirmation_date + "<br>"; 
                var confirmation_date = "<b>Confirmation Date: </b>" + employee_data.final_confirmation_date + "<br>"; 
                var contract_end = "<b>Contract End Date: </b>" + employee_data.contract_end_date + "<br>"; 
                var retirement_date = "<b>Date of Retirement: </b>" + employee_data.date_of_retirement + "<br>"; 
                var company_email = "<b>Company Email: </b>" + employee_data.company_email + "<br>"; 
                var employee_id = "<b>Status: </b>" + employee_data.status + "<br>"; 

                employee_data_display = image + employee_id + name + username + date_joined + dob + gender + status + employment_type + offer_date
            + confirmation_date + contract_end + retirement_date + company_email + employee_id;

            }

            document.getElementById("employee_data").innerHTML = employee_data_display;
        }}) 
}

// //store in session
// if (typeof(Storage) !== "undefined") {
//     // Store
//     localStorage.setItem("position_data", position_data_display);
// } else {
//     // Retrieve
//     var retreived_data = localStorage.getItem("position_data");
//     if (retreived_data != )
//     document.getElementById("result").innerHTML = "Sorry, your browser does not support Web Storage...";
// }
function searching(){
    var search_name = document.getElementById("search_name").value;
    var search_position = document.getElementById("search_position").value;
    searchThru(search_name, search_position);
}


function searchThru(search_name, search_position) {
    frappe.call({
        method: "organizational_management.api.search_employee",
        args: {
            search_name: search_name,
            search_position: search_position
        },
        callback: function(r) {
            var string = r.message
            if (string != "None") {
                var compare = string.page_name;
                

                frappe.call({
                    method: "organizational_management.api.get_required_search",
                    args: {
                        position2 : compare
                    },
                    callback: function(result) {
                        var positions = result.message;
                        var count = 0
                        var print_out = "";
                        var breaking = -1;
                        var reporting_to = "";

                        var child_array = new Array();
                        var count1 = 0
                        var level_ref = null;
                        var previous_li = "False";

                        for (count =  0 ; count < positions.length; count ++){

                            var position = positions[count];
                            
                            
                            var list_num = count;
                            var page_name = position.page_name;
                            var company = position.company;
                            var designation = position.designation;
                            var department = position.department;
                            var job_description = position.job_description;
                            var position_band = position.position_band;
                            var report_to = position.report_to;
                            var others_website = position.others_website;
                            var level = position.level;

                            if (level_ref == null){
                                level_ref = level;
                                console.log(level);
                            }


                            if (breaking == -1 ){
                            	print_out = print_out + "breaking = -1:  <ul>";

                            } else if (breaking == 0 ){
                            	print_out = print_out + "breaking = 0:  <ul>";
                            	breaking ++;
                            	level_ref = level;

                            	console.log(page_name);
                            	console.log(level);

                            } else {
                            	console.log(page_name);
                            	console.log(level);

                            }
                            

                            child_array.push(position);

                            print_out = print_out + "<li><span class='Collapsable'><a id = ' " + list_num + 
                            " ' value = '" + page_name + "," + company + ","
                             + department + "," + designation + "," + job_description
                             + ","  + position_band + "," + report_to + "," + others_website
                             + " 'onmouseover='mouseOver(this.id, this.value)'><b>" 
                             + designation + "</b><br>" +
                             +  department + "<br>" + company + "</a></span>" ;

                             

                             if (compare == page_name){
                                breaking = 0;
                            }

                            reporting_to = page_name;
                            count1 ++;

                            
                        }
                        // frappe.msgprint(print_out)


                        for (count = 0; count < position.length; count ++){
                            print_out = print_out + "</li></ul>"
                        }

                        // var test = name1[0];
                        document.getElementById("tree_root").innerHTML = print_out;
                        

                    }}) 


            }
        }}) 
}




