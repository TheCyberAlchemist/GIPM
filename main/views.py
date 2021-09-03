from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views import View
# Create your views here.
from .models import *
from .forms import *
from ajax_datatable.views import AjaxDatatableView

#region ########### Indent ###########
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
	template_name = "indent/indent_table.html"
	def get(self, request,po_id):
		po = purchase_order.objects.filter(pk=po_id).first()
		context= {
			"update":[],
			'all_indents': indent.objects.all().filter(PO__id=po_id),
			'po':po,
			'po_id':po_id,
		}
		return render(request,self.template_name,context)
	def post(self, request):
		pass

class indent_form(View):
	template_name = "indent/indent_form.html"
	context= {
		"update":[],
		'all_indents': indent.objects.all(),
		"all_item_description":item_description.objects.all(),
	}
	def get(self, request,po_id=None,indent_id=None):
		if indent_id: 
			instance = indent.objects.get(pk=indent_id)
			print(indent_id,"here in Update")
			self.context['update'] = instance
			self.context['success'] = False
			return render(request,self.template_name,self.context)
		else:
			self.context['update'] = []
			print(self.context['update'],"here in add")
			return render(request,self.template_name,self.context)

	def post(self, request,po_id=None,indent_id=None):
		po = purchase_order.objects.filter(pk=po_id).first()
		if indent_id:
			instance = indent.objects.get(pk=indent_id)
			form = add_indent(request.POST,instance=instance)
		else:
			form = add_indent(request.POST)
		if form.is_valid():
			temp = form.save(commit=False)
			temp.PO = po
			self.context['update'] = form.instance
			self.context['success'] = True
			temp.save()
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)
#endregion

#region ########### Purchase Order ###########
class PO_form(View):
	template_name = "po/PO_form.html"
	context= {
		"update":[],
		'all_vendors':vendor_details.objects.all(),
		'all_work_order':work_order.objects.all(),
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
			form = add_PO(request.POST)
		if form.is_valid():
			form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)

class PO_table(View):
	template_name = "po/PO_table.html"
	def get(self, request):
		context= {
			"update":[],
			'all_PO': purchase_order.objects.all(),
		}
		return render(request,self.template_name,context)
	def post(self, request):
		pass
#endregion

#region ########### Work-Order ###########
class WO_datatable(AjaxDatatableView):
	model = work_order
	title = 'work_order'
	length_menu = [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'all']]
	initial_order = [["wo_number","asc"]]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{
			'name': 'wo_number', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'WO Number',
		},
		{
			'name': 'description', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Description',
		},
		{
			'name': 'quantity', 
			'visible': True,
			'orderable': True,
			'searchable': False,		
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
			'name': 'is_complete', 
			'visible': True,
			'orderable': True,	
			'searchable': False,		
			'title': 'Completed',
		},
		{'name': 'Indent List', 'visible': True,'searchable': False, 'orderable': False},
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete',
			'visible': True,
			'searchable': False,
			'orderable': False
		}, # delete field
	]
	
	def get_initial_queryset(self, request=None):
		# po_id=request.REQUEST.get('po_id')

		queryset = self.model.objects.all()
		# queryset = queryset.filter(PO__id=po_id)
		# queryset = self.model.objects.all()
		return queryset
	
	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		row['net_value'] = f''' {obj.net_value()}'''

		row['Edit'] = f'''<td class="">
				<a href="../form/{obj.pk}" target="_blank">
				<img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
			</td>'''
		row['Indent List'] = f'''<td class="">
				<a href="{{url ('show_indent_table' ,args=[wo.pk])}}" target="_blank">
					<img src="../../static/Images/enter.png" style="width:19px;height:19px" alt="enter">
				</a>
			</td>'''
		row['Delete'] =f'''<div class="form-check" onclick="checkSelected()">
				<input class="form-check-input del_input" type="checkbox"
				name="del" value="{obj.pk}" input_name="{obj}">
			</div>'''
		return

	def render_row_details(self, pk, request=None):
		obj = self.model.objects.get(pk=pk)
		# fields = [f for f in self.model._meta.get_fields() if f.concrete]
		fields = {
			'Vendor':obj.vendor_id,
			'Comment':obj.comment,
			'PO Number':obj.incoming_po_number,
			'PO Date':obj.incoming_po_date,
			'Value':obj.value,
			'Tax':obj.tax,
			'Discount':obj.discount,
			'Other Expanses':obj.other_expanses,
		}
		fields = {k: v for k, v in fields.items() if v is not None}
		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:60%">'
		for key in fields:
		    html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		html += '</table>'
		return html

class WO_table(View):
	template_name = "WO/wo_table.html"
	context  = {}
	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,self.context)

	def post(self, request, *args, **kwargs):
		pks = request.POST.getlist("pks[]")
		for i in pks:
			obj = work_order.objects.filter(pk=i)[0]
			obj.delete()
		return JsonResponse({"deleted":True})

	
class WO_form(View):
	template_name = "WO/wo_form.html"
	context= {
		"update":[],
		'all_vendors':vendor_details.objects.all(),
		"all_item_description":item_description.objects.all(),
	}
	def get(self, request,wo_id=None, *args, **kwargs):
		if wo_id:
			instance = work_order.objects.get(pk=wo_id)
			self.context['update'] = instance
			self.context['success'] = False
			return render(request,self.template_name,self.context)
		else:
			self.context['update'] = []
			return render(request,self.template_name,self.context)
	
	def post(self, request,wo_id=None, *args, **kwargs):
		if wo_id:
			instance = work_order.objects.get(pk=wo_id)
			form = add_WO(request.POST,instance=instance)
		else:
			form = add_WO(request.POST)
		if form.is_valid():
			form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)
#endregion