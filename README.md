<<<<<<< HEAD
## organizational_management

Capture the organizational hierarchy in companies and have a view on the Delegation of Authorities when transactions are being performed




## What is organizational chart?

Organizational chart is a diagram that graphically represents the structure of an organization and the relation between and positions. By using the organizational chart, one is able to view each position's information and the employee's information tied to the position. One can also search any employee or position from the organization chart, and the result will show the hierarchy leading to the employee/position searched.


## How to use organizational chart?

1.	Create the Positions in the Position Doctype. "Board of Director" is the default root position and it is NOT TO BE EDITTED/DELETED. Set head to the position(s) directly under the "Board of Director". Use the Report To field to form the hierarchy. More details can be found below. 
2.  At Employee doctype, tag employee to the Position. More details can be found below.


## How to create a new Position?

1.	Navigate to Organizational Management > Position.
2.	Create New Doctype.
3.	Select desired Designation and Department. Title will be auto-populated. 
4.  Select which position the created position reports to via Report To field.
5.  Tick "head" if the position is to be mapped directly under "Board of Director". If "head" is not ticked, Report To field should not be left empty.

## How to tie an Employee to a Position?

1.	Navigate to desired Employee.
2.	Select the position of the employee at the "Position" field.
3.	Each position can only be assigned to one employee.

## How to view the Organization chart?

1.	Navigate to Organizational Management > Position.
2.  Select any position and click on "Navigate to Org Chart" button at the top right. 

## Features of the Organization chart:
1.	Home Button
-	Allow user to return to the full chart.
2.	Search Function
-	Allow user to search employee or position.
- Search can be done by Employee name or Position or both. If search is done by both, it will show error if 2 different positions are found.
- The search result will show all the hierarchies leading to the search target.
- Search target will be highlighted in red font.
3.	Toggle over
-	When you mouse move over any Position displayed, the position and employee information tied to that position will be showed in the side bar.


#### License

MIT
=======
# cloude8
Cloude8's Github Repository
>>>>>>> 16f29731e14e809d8257e662cf8a97ca2586d577
