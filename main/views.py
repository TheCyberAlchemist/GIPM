from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views import View
# Create your views here.
from .models import *
from .forms import *
from ajax_datatable.views import AjaxDatatableView

def home_page(request):
	return render(request, 'home.html')
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
			'name': 'Description',
			'foreign_field': 'item_description__description',
			'visible': True,
			'searchable': True,
			'placeholder':'description'
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
		wo_id=request.REQUEST.get('wo_id')

		queryset = self.model.objects.all()
		queryset = queryset.filter(WO__id=wo_id)
		# queryset = self.model.objects.all()
		return queryset
	
	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		row['net_value'] = f''' {obj.net_value()}'''
		row['Edit'] = f'''<td class="border-0">
				<a href="/wo/{obj.WO.pk}/indent/form/{obj.pk}"><img src="../../../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
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
			'PO Number':obj.PO,
			'Material Type':obj.material_type,
			'Item Description':obj.item_description,
			"Size":obj.size,
			"Thickness":obj.thickness,
			"Width":obj.width,
			"Internal Diameter":obj.internal_diameter,
			'Description':obj.description,
			'Value':obj.value,
			'Tax':obj.tax,
			'Discount':obj.discount,
			'Other Expanses':obj.other_expanses,
			"Weight":obj.get_weight()
		}
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:60%">'
		for key in fields:
		    html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		html += '</table>'
		return html

class indent_table_page(View):
	template_name = "indent/indent_table.html"
	def get(self, request,wo_id):
		wo = work_order.objects.filter(pk=wo_id).first()
		context= {
			"update":[],
			'all_indents': indent.objects.all().filter(WO__id=wo_id),
			'wo':wo,
			'wo_id':wo_id,
		}
		return render(request,self.template_name,context)
	def post(self, request,wo_id):
		pks = request.POST.getlist("pks[]")
		for i in pks:
			obj = indent.objects.filter(pk=i).first()
			# obj.quantity=3
			# obj.save()
			obj.delete()
		return JsonResponse({"deleted":True})

class indent_form(View):
	template_name = "indent/indent_form.html"
	def get(self, request,wo_id=None,indent_id=None):
		self.context= {
			"update":[],
			'all_indents': indent.objects.all(),
			"all_item_description":item_description.objects.all(),
			'wo':work_order.objects.get(pk=wo_id),
		}
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

	def post(self, request,wo_id=None,indent_id=None):
		self.context= {
			"update":[],
			'all_indents': indent.objects.all(),
			"all_item_description":item_description.objects.all(),
		}
		wo = work_order.objects.filter(pk=wo_id).first()
		if indent_id:
			instance = indent.objects.get(pk=indent_id)
			form = add_indent(request.POST,instance=instance)
			if not wo:
				wo = instance.WO
		else:
			form = add_indent(request.POST)
		if form.is_valid():
			temp = form.save(commit=False)
			temp.WO = wo
			item_desc,_=item_description.objects.get_or_create(
				description=request.POST.get("item_description")
			)
			print(item_desc,_)
			temp.item_description = item_desc
			self.context['update'] = form.instance
			self.context['success'] = True
			print(temp.item_description)
			temp.save()
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)

#endregion

#region ########### Purchase Order ###########
class PO_datatable(AjaxDatatableView):
	model = purchase_order
	title = 'Purchase Order'
	length_menu = [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'all']]
	initial_order = [["po_number","asc"]]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{
			'name': 'po_number',
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'PO Number',
		}, # po number
		{
			'name': 'Vendor',
			'foreign_field': 'vendor_id__vendor_name',
			'visible': True,
			'searchable': True,
			'placeholder':'Vendor'
		}, # vendor
		{
			'name': 'quantity', 
			'visible': True,
			'orderable': True,
			'searchable': False,
			'title': 'Quantity',
		}, # quantity
		{
			'name': 'po_date',
			'visible': True,
			'searchable': False,
			'orderable': True,
			'title': 'PO Date',
		}, # po date
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
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete',
			'visible': True,
			'searchable': False,
			'orderable': False
		}, # delete field
	]
	
	def get_initial_queryset(self, request=None):
		return queryset
	
	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		
		row['net_value'] = f''' {obj.net_value()}'''

		row['Edit'] = f'''<td class="">
				<a href="../form/{obj.pk}" target="_blank">
				<img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
			</td>'''
		row['Indent List'] = f'''<td class="">
				<a href="indent/table/{obj.pk}" target="_blank">
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
			'Description':obj.description,
			'Comment':obj.comment,
			'PO Number':obj.incoming_po_number,
			'PO Date':obj.incoming_po_date,
			'Value':obj.value,
			'Tax':obj.tax,
			'Discount':obj.discount,
			'Other Expanses':obj.other_expanses,
		}
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:60%">'
		for key in fields:
		    html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		html += '</table>'
		return html

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
				<a href="/wo/{obj.pk}/indent/table/" target="_blank">
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
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
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
		tempdict = self.request.POST.copy()
		tempdict['value'] = 12
		print(tempdict['value'])
		if wo_id:
			instance = work_order.objects.get(pk=wo_id)
			form = add_WO(tempdict,instance=instance)
		else:
			form = add_WO(tempdict)
		if form.is_valid():
			# form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.instance.value)
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)
#endregion