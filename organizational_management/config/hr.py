from __future__ import unicode_literals
from frappe import _

def get_data():
        return [
               {
					"label": _("Organisational Management"),
                    "icon": "icon-star",
                    "items": [
						{
							"type": "doctype",
							"name": "Band",
							"description": _("Assign Salary Ranges to Band."),
						},
						{
							"type": "doctype",
							"name": "Position",
							"description": _("Setup Positions in company"),
						},
						{
							"type": "doctype",
							"name": "Approval Limit",
							"description": _("Set approval limit for system role"),
						},
						]
                },
 	]
  
