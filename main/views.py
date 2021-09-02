from django.shortcuts import render
from .models import *
from django.views import View
# Create your views here.
from .models import *
from .forms import *
from ajax_datatable.views import AjaxDatatableView

class PO_table(View):
	template_name = "PO_table.html"
	def get(self, request):
		context= {
			"update":[],
			'all_PO': purchase_order.objects.all(),
		}
		return render(request,self.template_name,context)
	def post(self, request):
		pass

class indent_table(AjaxDatatableView):
	model = indent
	title = 'Indent'
	length_menu = [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'all']]
	initial_order = [["recived","asc"]]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{
			'name': 'material_shape', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Shape',
		},
		{
			'name': 'quantity', 
			'visible': True,			
			'searchable': False,
			'orderable': False,
			'title': 'Quantity',
		},
		{
			'name': 'net_value', 
			'visible': True,
			'orderable': True,
			'searchable': False,		
			'title': 'Net Value',
		},
		{
			'name': 'recived', 
			'visible': True,
			'orderable': True,	
			'searchable': False,		
			'title': 'Recived',
		},
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete',
			'visible': True,
			'searchable': False,
			'orderable': False
		}, # delete field
	]
	def get_initial_queryset(self, request=None):
		po_id=request.REQUEST.get('po_id')

		queryset = self.model.objects.all()
		queryset = queryset.filter(PO__id=po_id)
		# queryset = self.model.objects.all()
		return queryset
	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		row['net_value'] = f''' {obj.net_value()}'''
		row['Edit'] = f'''<td class="border-0">
				<a href="../../form/{obj.pk}" target="_blank"><img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
			</td>'''
		return

class indent_table_page(View):
	template_name = "indent_table.html"
	def get(self, request,po_id):
		context= {
			"update":[],
			'all_indents': indent.objects.all().filter(PO__id=po_id),
			'po_id':po_id,
		}
		return render(request,self.template_name,context)
	def post(self, request):
		pass

class indent_form(View):
	template_name = "indent_form.html"
	context= {
		"update":[],
		'all_indents': indent.objects.all(),
		'all_vendors':vendor_details.objects.all(),
		'all_work_order':work_order.objects.all(),
		"all_item_description":item_description.objects.all(),
	}
	def get(self, request,po_id=None,indent_id=None):
		if indent_id: 
			instance = indent.objects.get(pk=indent_id)
			print(indent_id)
			self.context['update'] = instance
			self.context['success'] = False
		return render(request,self.template_name,self.context)

	def post(self, request,po_id=None,indent_id=None):
		if indent_id:
			instance = indent.objects.get(pk=indent_id)
			form = add_indent(request.POST,instance=instance)
		else:
			form = add_indent(request.POST)
		if form.is_valid():
			form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)

class PO_form(View):
	template_name = "PO_form.html"
	context= {
		"update":[],
		'all_vendors':vendor_details.objects.all(),
	}
	def get(self, request,po_id=None):
		if po_id: 
			instance = purchase_order.objects.get(pk=po_id)
			self.context['update'] = instance
			self.context['success'] = False
		return render(request,self.template_name,self.context)

	def post(self, request,po_id=None):
		if po_id:
			instance = purchase_order.objects.get(pk=po_id)
			form = update_PO(request.POST,instance=instance)
		else:
			form = add_indent(request.POST)
		if form.is_valid():
			form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)
