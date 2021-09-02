from django.forms import ModelForm
from .models import *
class add_indent(ModelForm):
	class Meta:
		model = indent
		fields = '__all__'
