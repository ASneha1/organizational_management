# -*- coding: utf-8 -*-
# Copyright (c) 2015, Cloude8 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe import _
import frappe.defaults

class ApprovalLimit(Document):
	def autoname(self):
		self.name = self.role + ' - ' + self.company + ' - ' + self.transaction + ' - ' + str(self.value)
