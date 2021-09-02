from django.db import models

class vendor_details(models.Model):
	vendor_name = models.TextField(null=True, blank=True)
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
		return f"{self.vendor_name} ({self.contact_person})"

	class Meta:
		verbose_name_plural = "Vendor Details"
		constraints = [
			models.UniqueConstraint(fields=['vendor_name', 'contact_person'], name='Vendor name and contact person cannot be same.'),
		]

class purchase_order(models.Model):
	po_number = models.CharField(max_length=200,null=True, blank=True)
	po_date = models.DateField(null=True, blank=True)
	vendor_id = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	is_complete = models.BooleanField(default=False)
	def __str__(self):
		return f"{self.po_number} [{self.vendor_id.vendor_name}]"
	
	def save(self,*args, **kwargs):
		super(purchase_order, self).save(*args, **kwargs)
		if not self.po_number:
			self.po_number = "GI-"+ str(self.pk)
			super(purchase_order, self).save(*args, **kwargs)



class order(models.Model):
	'''base class for other models having orders.\n
	`order_no,date,quantity,tax,etc.`
	'''
	# po_number = models.CharField(max_length=200,null=True, blank=True)
	# po_date = models.DateField(null=True, blank=True)
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
	''' Class for incoming work orders '''
	PO = models.ForeignKey(purchase_order,on_delete=models.CASCADE)
	# party_name = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return "%s"%(self.PO)

class item_description(models.Model):
	'class of items which shoud be addable in for the indent'
	description = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.description

class standard_weight(models.Model):
	material_shape = models.TextField(null=True, blank=True)
	size = models.FloatField(null=True, blank=True)
	weight_pmm = models.FloatField(null=True, blank=True)
	class Meta:
		verbose_name_plural = "Standard Weight"
		constraints = [
			models.UniqueConstraint(fields=['size', 'material_shape'], name='Shape and size cannot be same.'),
		]
	def __str__(self):
		return f"{self.material_shape} ({self.size})"

class indent(order):
	''' class for outgoing work orders '''

	PO = models.ForeignKey(purchase_order,on_delete=models.CASCADE)
	# vendor_name = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	# dropdown of vendor class 
	work_order_id = models.ForeignKey(work_order,on_delete=models.SET_NULL,null=True, blank=True)
	# FK to specify the work_order for which the indent is made
	# show a dropdown of all the active work_orders

	recived = models.BooleanField(default=False)
	comment = models.TextField(null=True, blank=True)
	material_shape = models.TextField(null=True, blank=True)
	# dropdown must contain
	# Round,Plate,SQ Bar,Pipe,BF,Labour,ISMC,ISMB,ISA,Bolt,Nut ...

	material_type = models.TextField(null=True, blank=True)
	item_description = models.ForeignKey(item_description,on_delete=models.SET_NULL,null=True, blank=True)
	# dropdown for all objects
	size = models.FloatField(null=True, blank=True)
	thickness = models.FloatField(null=True, blank=True)
	width = models.FloatField(null=True, blank=True)
	internal_diameter = models.FloatField(null=True, blank=True)

	def get_weight(self):
		''' the function returning the weights respective to material_shape'''
		T = self.thickness
		S = self.size
		W = self.width
		ID = self.internal_diameter
		Q = self.quantity
		if self.material_shape == "Round":
			return (S*S*T*0.00000616)*Q
		elif self.material_shape == "Plate" or self.material_shape == "SQ Bar":
			return (S*T*W*0.00000786)*Q
		elif self.material_shape == "Pipe":
			return ((S*S - ID*ID)*T*0.00000616)*Q
		elif self.material_shape == "Labour" or self.material_shape == "BF":
			return Q
		elif self.material_shape in ["ISMC","ISMB","ISA","Bolt","Nut"]:
			w_pmm = standard_weight.objects.filter(material_shape=shape,size=S).first().weight_pmm
			return w_pmm * T

