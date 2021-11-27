from django.db import models
# import jsonfield

#region ############ JSONField ############
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json

class JSONField(models.TextField):
    """
    JSONField es un campo TextField que serializa/deserializa objetos JSON.
    Django snippet #1478

    Ejemplo:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)

        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """
    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value

#endregion

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
	comment = models.TextField(null=True, blank=True)

	def __str__(self):
		return f"{self.vendor_name} ({self.contact_person})"

	class Meta:
		verbose_name_plural = "Vendor Details"
		constraints = [
			models.UniqueConstraint(fields=['vendor_name', 'contact_person'], name='Vendor name and contact person cannot be same.'),
		]

class item_description(models.Model):
	'class of items which shoud be addable in for the indent'
	description = models.TextField(unique=True)
	estimated_value = models.FloatField(default=0,null=True, blank=True)

	def __str__(self):
		if self.description:
			return str(self.description)
		else:
			return ""


class order(models.Model):
	'''base class for other models having orders.\n
	`order_no,date,quantity,tax,etc.`
	'''
	# po_number = models.CharField(max_length=200,null=True, blank=True)
	# po_date = models.DateField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	quantity = models.FloatField(default=0,null=True, blank=True)
	unit = models.TextField(null=True, blank=True)
	value = models.FloatField(default=0,null=True, blank=True)
	tax = models.FloatField(default=0,null=True, blank=True)
	discount = models.FloatField(default=0,null=True, blank=True)
	other_expanses  = models.FloatField(default=0,null=True, blank=True)

	def gross_value(self):
		'return the gross value of the order \n ((value-discount) * quantity)'
		# is overwritten in indent to use weight instead of quantity
		temp = (self.discounted_total() * self.quantity) + self.other_expanses
		return round(temp,2) if temp else 0

	def discounted_total(self):
		'''return the discounted total of the order (net_val - discount)'''
		temp = self.value - self.discount
		return round(temp,2) if temp else 0

	def tax_amount(self):
		'return the tax amount of the order (gross_value * tax)'
		temp = (self.gross_value()) * self.tax/100
		return round(temp,2) if temp else 0

	def net_value(self):
		'return the tax amount of the order (gross_value + tax)'
		temp = self.gross_value() + self.tax_amount()
		# (value-discount * quantity) + (((value-discount) * quantity) * tax)
		temp = temp
		return round(temp,2) if temp else 0

	def save(self,*args, **kwargs):
		self.quantity = self.quantity if self.quantity else 0
		self.value = self.value if self.value else 0
		self.tax = self.tax if self.tax else 0
		self.discount = self.discount if self.discount else 0
		self.other_expanses = self.other_expanses if self.other_expanses else 0
		super(order, self).save()

class work_order(order):
	''' Class for incoming work orders '''
	# PO = models.ForeignKey(purchase_order,on_delete=models.CASCADE)
	# party_name = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	wo_number = models.CharField(max_length=200,null=True, blank=True,unique=True)
	vendor_id = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	incoming_po_number = models.CharField(max_length=200,null=True, blank=True)
	incoming_po_date = models.DateField(null=True, blank=True)

	comment = models.TextField(null=True, blank=True)

	is_complete = models.BooleanField(default=False)

	def __str__(self):
		return "%s"%(self.wo_number)

class purchase_order(models.Model):
	po_number = models.CharField(max_length=200,null=True, blank=True)
	po_date = models.DateField(null=True, blank=True)
	vendor_id = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	is_complete = models.BooleanField(default=False)
	# work_order_id = models.ForeignKey(work_order,on_delete=models.SET_NULL,null=True, blank=True)
	# FK to specify the work_order for which the indent is made
	# show a dropdown of all the active work_orders

	def __str__(self):
		if self.vendor_id:
			return f"{self.po_number} [{self.vendor_id.vendor_name}]"
		else:
			return f"{self.po_number}"
	
	def get_received_quantity(self):
		pass
	
	def get_date(self):
		return self.po_date.strftime("%d-%m-%Y") if self.po_date else "-----"
		
	def save(self,*args, **kwargs):
		super(purchase_order, self).save(*args, **kwargs)
		if not self.po_number:
			if self.pk < 100:
				self.po_number = "GI-00"+ str(self.pk)
			else:
				self.po_number = "GI-"+ str(self.pk)
			super(purchase_order, self).save(*args, **kwargs)

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
	locked = models.BooleanField(default=False)
	
	PO = models.ForeignKey(purchase_order,on_delete=models.CASCADE,null=True, blank=True)
	WO = models.ForeignKey(work_order,on_delete=models.CASCADE)
	# vendor_id = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	# dropdown of vendor class 
	recived_quantity = models.FloatField(default=0,null=True, blank=True)
	recived = models.BooleanField(default=False)
	comment = models.TextField(null=True, blank=True)
	material_shape = models.TextField()
	# dropdown must contain 
	# Round,Plate,SQ Bar,Pipe,BF,Labour,ISMC,ISMB,ISA,Bolt,Nut ...

	material_type = models.TextField(null=True, blank=True)
	item_description = models.ForeignKey(item_description,on_delete=models.SET_NULL,null=True, blank=True)
	# dropdown for all objects
	size = models.FloatField(default=0,null=True, blank=True)
	thickness = models.FloatField(default=0,null=True, blank=True)
	width = models.FloatField(default=0,null=True, blank=True)
	internal_diameter = models.FloatField(default=0,null=True, blank=True)

	def gross_value(self):
		'return the gross value of the order \n ((value-discount) * weight)'
		# overwritting the gross_value function to use weight
		temp = (self.discounted_total() * self.get_weight()) + self.other_expanses
		return round(temp,2) if temp else 0

	def get_weight(self):
		'''the function returning the weights respective to material_shape'''
		round_no = lambda x: round(x,3)
		T = self.thickness or 0
		S = self.size or 0
		W = self.width or 0
		ID = self.internal_diameter or 0
		Q = self.quantity or 0
		if self.material_shape == "Round":
			return round_no((S*S*T*0.00000616)*Q)
		elif self.material_shape == "Plate" or self.material_shape == "SQ Bar":
			return round_no((S*T*W*0.00000786)*Q)
		elif self.material_shape == "Pipe":
			return round_no(((S*S - ID*ID)*T*0.00000616)*Q)
		elif self.material_shape == "Labour" or self.material_shape == "BF":
			return Q
		elif self.material_shape in ["ISMC","ISMB","ISA","Bolt","Nut"]:
			w_pmm = standard_weight.objects.filter(material_shape=shape,size=S).first().weight_pmm
			return round_no(w_pmm * T * Q)
		return 0
	
	def __str__(self):
		if self.id:
			return f"{self.pk} [{self.item_description}]"

	def get_remaining_quantity(self):
		return float(self.get_weight() - self.recived_quantity)

	def save(self,*args, **kwargs):
		# update the estimate for the item_description 
		self.item_description.estimated_value = self.value
		self.item_description.save()
		
		if self.recived_quantity >= self.quantity:
			self.recived = True
		super(indent, self).save(*args, **kwargs)

class grn(order):
	vendor_id = models.ForeignKey(vendor_details,on_delete=models.SET_NULL,null=True, blank=True)
	invoice_no = models.CharField(max_length=200,null=True, blank=True)
	indent_id = models.ForeignKey(indent,on_delete=models.CASCADE,null=True, blank=True)
	grn_date = models.DateField(null=True, blank=True)
	def __str__(self):
		if self.invoice_no:
			return f"{self.invoice_no}"
		else:
			return str(self.pk)
	
	def get_save_messages(self,quantity):
		'returns the respective string checking the quantity recived '
		quantity = float(quantity)
		if quantity > self.indent_id.get_remaining_quantity():
			remaining = quantity - self.indent_id.get_remaining_quantity()
			return f"Extra units received! {int(remaining)} units stored in STOCK."
		return "Saved GRN and updated indent."


	class Meta:
		verbose_name_plural = "GRN"
		constraints = [
			models.UniqueConstraint(fields=['invoice_no', 'indent_id'], name='Same invoice cannot be in the same indent.'),
		]


	def save(self,*args, **kwargs):
		# indent_id = self.indent_id
		# print("here in grn :: ",indent_id.get_remaining_quantity())
		super(grn, self).save(*args, **kwargs)

class assembly(models.Model):
	# https://stackoverflow.com/questions/14666199/how-do-i-create-multiple-model-instances-with-django-rest-framework
	items = models.ManyToManyField(item_description)
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank=True)
	item_json = JSONField()
	# item_json = {
		# pk:{
			# "quantity":1
		# },
	# }
	estimate_value = models.FloatField(default=0,null=True, blank=True)
	def __str__(self):
		return f'{self.name}'
	
	class Meta:
		verbose_name_plural = "Assembly"
		constraints = [
			# models.UniqueConstraint(fields=['vendor_name', 'contact_person'], name='Vendor name and contact person cannot be same.'),
		]

	def get_total_estimate(self):
		total_estimate = 0
		for item in self.items.all():
			total_estimate += item.get_estimated_value()
		return total_estimate

class plan(models.Model):
	name = models.CharField(max_length=200)
	assemblies = models.ManyToManyField(assembly)
	item_state = JSONField(null=True, blank=True)
	estimate = models.FloatField(default=0,null=True, blank=True)

	def __str__(self):
		return f'{self.name}'

	class Meta:
		verbose_name_plural = "Plan"
		constraints = [
			# models.UniqueConstraint(fields=['vendor_name', 'contact_person'], name='Vendor name and contact person cannot be same.'),
		]
	
