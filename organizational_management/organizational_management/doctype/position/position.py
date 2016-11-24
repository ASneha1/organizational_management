
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
#from frappe.website.website_generator import WebsiteGenerator
from frappe.website.render import clear_cache

class Position(Document):
	
	def validate(self):

		if self.head == 1:
			self.report_to = "board of director"
		else:
			temp = self.report.lower()		
			self.report_to = temp.replace(',', '' )


		self.name = self.title
		temp = self.name.lower()
		
		self.page_name = temp.replace( ',','')
		
		y= frappe.get_list("Position",fields=["*"],filters = [["report_to","=",self.name]])

		for position in y :
			if self.report_to == position.name:
				frappe.throw (_("Conflict occur at Report to"))
		if self.head != 1:
			if self.report_to == "" or self.report_to is None :
					frappe.throw (_("Not head position must have report to"))



