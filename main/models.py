from django.db import models

class vendor_details(models.Model):
	address = models.TextField(null=True, blank=True)
	contact_person = models.TextField(null=True, blank=True)
	contact_number = models.TextField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	gst_no = models.TextField(null=True, blank=True)
	name_of_bank = models.TextField(null=True, blank=True)
	acc_no = models.TextField(null=True, blank=True)
	ifsc_code = models.TextField(null=True, blank=True)
	branch = models.TextField(null=True, blank=True)

	def __str__(self):
		return "%s - %s"%(self.contact_person,self.contact_number)

class order(models.Model):
	po_number = models.IntegerField(null=True, blank=True)
	po_date = models.DateField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	unit = models.TextField(null=True, blank=True)
	value = models.IntegerField(null=True, blank=True)
	tax = models.IntegerField(null=True, blank=True)
	discount = models.IntegerField(null=True, blank=True)
	other_expanses  = models.IntegerField(default=0)

	def gross_value(self):
		'return the gross value of the order \n ((value-discount) * quantity)'
		return self.discounted_total() * self.quantity

	def discounted_total(self):
		'''return the discounted total of the order (net_val - discount)'''
		return self.value - self.discount

	def tax_amount(self):
		'return the tax amount of the order (net_value * tax)'
		return (self.gross_value()+ self.other_expanses) * self.tax/100

	def net_value(self):
		'return the tax amount of the order (gross_value + tax)'
		return self.gross_value() + self.tax_amount()

class work_order(order):
	party_name = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	def __str__(self):
		return "%s--%d "%(self.po_number,self.party_name)

class indent(order):
	work_order_id = models.ForeignKey(work_order,on_delete=models.SET_NULL,null=True, blank=True)

	material_shape = models.TextField(null=True, blank=True)
	material_type = models.TextField(null=True, blank=True)

	size = models.IntegerField()
	thickness = models.IntegerField()
	width = models.IntegerField()
	internal_diameter = models.IntegerField()

	def get_weight():
		pass


class size(models.Model):
	pass