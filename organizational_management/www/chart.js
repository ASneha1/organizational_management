function mouseOver(id, value) {
    frappe.call({
        method: "organizational_management.api.get_employee",
        args: {
            id: id,
            value: document.getElementById(id).getAttribute("value")
        },
        callback: function(r) {
            document.getElementById("position_data").style = "float: middle;";


            var position = document.getElementById(id).getAttribute("value1");
            var details = position;
            var page_name = "<b>ID: </b>" + details + "<br>"; 

            var Company = document.getElementById(id).getAttribute("value2");
            details = Company;
            var company = "<b>Company: </b>" + details+ "<br>"; 

            var Department = document.getElementById(id).getAttribute("value3");
            details = Department;
            var department = "<b>Department: </b>" + details + "<br>"; 

            var Designation = document.getElementById(id).getAttribute("value4");
            details = Designation;
            var designation = "<b>Designation: </b>" + details + "<br>"; 

            var Job = document.getElementById(id).getAttribute("value5");
            details = Job;
            var job_description = "<b>Job Description: </b>" + details + "<br>"; 

            var Band = document.getElementById(id).getAttribute("value6");
            details = Band;
            var position_band = "<b>Position Band: </b>" + details + "<br>"; 

            var Report = document.getElementById(id).getAttribute("value7");
            details = Report;
            var report_to = "<b>Report To: </b>" + details + "<br>"; 

            var position_data_display =  page_name + company + department + designation + job_description + position_band + report_to;
            document.getElementById("position_data").innerHTML = position_data_display;

            var employee_data_display = "";
            var employee_data = r.message;

            if (employee_data == -1){
                employee_data_display = "No Employee tagged to this position";
		employee_data_image= "";
 		document.getElementById("employee_picture").innerHTML = employee_data_image; 
		document.getElementById("employee_data").innerHTML = employee_data_display;  

            } else {
                var image = "<img src ='" + employee_data.image + "'><br>"; 
                var employee_id = "<b>ID: </b>" + employee_data.employee + "<br>"; 
                var name = "<b>Name: </b>" + employee_data.salutation + " " + employee_data.employee_name + "<br>"; 
                var username = "<b>Username: </b>" + employee_data.user_id + "<br>"; 
                var date_joined = "<b>Date Joined: </b>" + employee_data.date_of_joining + "<br>"; 
                var dob = "<b>Date of Birth: </b>" + employee_data.date_of_birth + "<br>"; 
                var gender = "<b>Gender: </b>" + employee_data.gender + "<br>"; 
                var status = "<b>Status: </b>" + employee_data.status + "<br>"; 
                var employment_type = "<b>Employment Type: </b>" + employee_data.employment_type + "<br>"; 
                var offer_date = "<b>Offer Date: </b>" + employee_data.scheduled_confirmation_date + "<br>"; 
                var confirmation_date = "<b>Confirmation Date: </b>" + employee_data.final_confirmation_date + "<br>"; 
                var contract_end = "<b>Contract End Date: </b>" + employee_data.contract_end_date + "<br>"; 
                var retirement_date = "<b>Date of Retirement: </b>" + employee_data.date_of_retirement + "<br>"; 
                var company_email = "<b>Company Email: </b>" + employee_data.company_email + "<br>"; 
		employee_data_image = image;
                employee_data_display = employee_id + name + username + dob  + employment_type + company_email;
	    var employee_picture= employee_data;
           	 document.getElementById("employee_picture").innerHTML = employee_data_image; 
		document.getElementById("employee_data").innerHTML = employee_data_display;

            }
	     
	             
        }}) 
}

function mouseOver_empty() {
		 document.getElementById("position_data").innerHTML = "";	
				document.getElementById("employee_picture").innerHTML = ""; 
 		document.getElementById("employee_data").innerHTML = ""; 

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
			    var name =position.name;
                            var page_name = position.page_name;
                            var company = position.company;
                            var designation = position.designation;
                            var department = position.department;
                            var job_description = position.job_description;
                            var position_band = position.position_band;
                            var report_to = position.report;
                            var others_website = position.others_website;
                            var level = position.level;
                            var add_value = "No";

                            if (level_ref == null){
                                level_ref = level;
                                console.log(level);
                            }


                            if (breaking == -1 ){
                            	print_out = print_out + "<ul>";

                            } else if (breaking == 0 ){
                            	print_out = print_out + "<ul>";
                            	breaking ++;
                            	level_ref = level;

                            	console.log(page_name);
                            	console.log(level);

                            } else {
                            	console.log(page_name);
                            	console.log(level);

                            	if (level == level_ref + 1){
                            		print_out = print_out + "<ul>";
                            		level_ref ++;

                            	} else if (level == level_ref - 1){
                            		print_out = print_out  + "</li></ul>";
                            		level_ref --;
                            	} else {
                            		var difference = level_ref - level;

                            		for (i = 0; i < difference; i++) { 
                            		    print_out = print_out + "</ul>";
                            		    level_ref --;
                            		}

                            		print_out = print_out + "</li>";
                            	}

                            }



                            child_array.push(position);

			    if ( page_name == compare )
			    {
			

                            print_out = print_out + "<li><span class='Collapsable'><c id = ' " + list_num + 
                            " ' value = '" + page_name + "," + company + ","
                             + department + "," + designation + "," + job_description
                             + ","  + position_band + "," + report_to + "," + others_website
                             + " ' value2 = '" + company + "' value3= '" + department + "' value4 ='" + designation +"' value5 = '"+ job_description +" ' value6 ='" + position_band + " ' value7 = '" + report_to + " ' value1 = '" + name + " ' onmouseover='mouseOver(this.id, this.value)'><b>" 
                             + designation + "</b><br>"
                             +  department + "<br>" + company + "</c></span>" ;
			    }
			    else if ( page_name == "board of director"){
                            print_out = print_out + "<li><span class='Collapsable'><a id = ' " + list_num + 
                            " ' value = '" + page_name + "," + company + ","
                             + department + "," + designation + "," + job_description
                             + ","  + position_band + "," + report_to + "," + others_website
                             + " 'onmouseover='mouseOver_empty()'><br><b> Board of Director </b><br><br></a></span>" ;
			    }
			    else {
		
                                                         print_out = print_out + "<li><span class='Collapsable'><a id = ' " + list_num + 
                            " ' value = '" + page_name + "," + company + ","
                             + department + "," + designation + "," + job_description
                             + ","  + position_band + "," + report_to + "," + others_website
                             + " ' value2 = '" + company + "' value3= '" + department + "' value4 ='" + designation +"' value5 = '"+ job_description +" ' value6 ='" + position_band + " ' value7 = '" + report_to + " ' value1 = '" + name + " ' onmouseover='mouseOver(this.id, this.value)'><b>" 
                             + designation + "</b><br>"
                             +  department + "<br>" + company + "</a></span>" ;
				}


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


$(".Collapsable").click(function () {

        $(this).parent().children().toggle();
        // $(this).text("Collapsed");
        $(this).toggle();
        // $(this).css("background-color", "yellow");

    });



