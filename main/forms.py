from django.forms import ModelForm
from .models import *
class add_indent(ModelForm):
	class Meta:
		model = indent
		fields = '__all__'

class add_PO(ModelForm):
	class Meta:
		model = purchase_order
		fields = '__all__'

class update_PO(ModelForm):
	class Meta:
		model = purchase_order
		fields = ['po_date',"is_complete"]
