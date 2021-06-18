from django.shortcuts import render
from .models import *
from django.views import View
# Create your views here.

class indent_page(View):
	template_name = "indent.html"
	def get(self, request):
		context= {
			"update":[],
		}
		return render(request,self.template_name,context)
	def post(self, request):
		pass
