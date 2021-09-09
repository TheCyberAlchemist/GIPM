from django.forms import ModelForm
from .models import *
class add_indent(ModelForm):
	class Meta:
		model = indent
		fields = '__all__'
		exclude = ('PO','WO','item_description')
class add_PO(ModelForm):
	class Meta:
		model = purchase_order
		fields = '__all__'
		
class update_PO(ModelForm):
	class Meta:
		model = purchase_order
		fields = ['po_date',"is_complete"]

class add_WO(ModelForm):
	class Meta:
		model = work_order
		fields = '__all__'

class add_vendor(ModelForm):
	class Meta:
		model = vendor_details
		fields = '__all__'

class add_grn(ModelForm):
	class Meta:
		model = grn
		fields = '__all__'