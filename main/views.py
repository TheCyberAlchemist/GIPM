from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.views import View
from django.db.models import Q
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
	length_menu = [[25, 50, 100, -1], [25, 50, 100, 'all']]
	initial_order = [["recived","asc"]]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'pk',
			'visible': True,
			'searchable': False,
			'orderable': True,
			'title': 'Indent Number',
		}, # pk
		{
			'name': 'material_shape', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Shape',
		}, # material_shape
		{
			'name': 'Description',
			'foreign_field': 'item_description__description',
			'visible': True,
			'searchable': True,
			'placeholder':'description'
		}, # Description
		{
			'name': 'weight', 
			'visible': True,			
			'searchable': False,
			'orderable': False,
			'title': 'Weight',
		}, # weight
		{
			'name': 'size', 
			'visible': True,			
			'searchable': False,
			'orderable': False,
			'title': 'Size',
		}, # size
		{
			'name': 'thickness', 
			'visible': True,			
			'searchable': False,
			'orderable': False,
			'title': 'THK',
		}, # thickness
		{
			'name': 'quantity', 
			'visible': True,			
			'searchable': False,
			'orderable': False,
			'title': 'Qut',
		}, # quantity
		{
			'name': 'net_value', 
			'visible': True,
			'orderable': False,
			'searchable': False,		
			'title': 'Net Val',
			'className': 'currency',
		}, # net_value
		{
			'name': 'recived', 
			'visible': True,
			'orderable': True,	
			'searchable': False,		
			'title': 'Recived',
		}, # recived
		{'name': 'Add GRN', 'visible': True,'searchable': False, 'orderable': False},
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete',
			'visible': True,
			'searchable': False,
			'orderable': False,
			"title":"DEL"
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
		get_str = lambda x: x if x else "--"
		row['net_value'] = f''' {obj.net_value()}'''
		row['size'] = get_str(obj.size)
		row['thickness'] = get_str(obj.thickness)

		row['weight'] = f''' {obj.get_weight()}'''
		row['Add GRN'] = f'''<td class="">
			<a href="/indent/{obj.pk}/grn/form/">
				<img src="../../../../static/Images/enter.png" style="width:19px;height:19px" alt="enter">
			</a>
		</td>'''
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
			"Recived": obj.recived_quantity,
			'Material Type':obj.material_type,
			'Item Description':obj.item_description,
			"Size":obj.size,
			"Thickness":obj.thickness,
			"Width":obj.width,
			"Internal Diameter":obj.internal_diameter,
			'Description':obj.description,
			'Tax':str(obj.tax)+"%",
			"Comment":obj.comment,
		}
		currency={
			'Value':obj.value,
			'Discount':obj.discount,
			'Other Expanses':obj.other_expanses,
		}
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:60%">'
		html += '<tr><td class="">PO Number</td><td class=""><a href = "/po/table/">%s</a></td></tr>' % (obj.PO)
		for key in fields:
		    html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		for key in currency:
			html += '<tr><td class="">%s</td><td class="currency">%s</td></tr>' % (key, currency[key])
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
		wo = work_order.objects.filter(pk=wo_id).first()
		self.context= {
			"update":[],
			'all_indents': indent.objects.all(),
			"all_item_description":item_description.objects.all(),
			'wo':wo,
		}
		tempdict = self.request.POST.copy()
		tempdict['value'] = tempdict['value'].replace(',', '').replace("₹","")
		if indent_id:
			instance = indent.objects.get(pk=indent_id)
			form = add_indent(tempdict,instance=instance)
			if not wo:
				wo = instance.WO
		else:
			form = add_indent(tempdict)
		if form.is_valid():
			temp = form.save(commit=False)
			temp.WO = wo
			item_desc,_=item_description.objects.get_or_create(
				description=tempdict.get("item_description")
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
	length_menu = [[25, 50, 100, -1], [25, 50, 100, 'all']]
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
			'name': 'remaining_quantity', 
			'visible': True,
			'orderable': True,
			'searchable': False,
			'title': 'Remaining Quantity',
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
			'orderable': False,
			'searchable': False,		
			'title': 'Net Value',
			'className': 'currency',
		},# net_value
		{
			'name': 'is_complete', 
			'visible': True,
			'orderable': True,	
			'searchable': False,		
			'title': 'Completed',
		},
		{'name': 'Print', 'visible': True,'searchable': False, 'orderable': False},
		{'name': 'Edit', 'visible': True,'searchable': False, 'orderable': False},
		{
			'name':'Delete',
			'visible': True,
			'searchable': False,
			'orderable': False
		}, # delete field
	]
	
	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		net_value = 0
		total_quantity,remaining_quantity = 0,0
		for indent in obj.indent_set.all():
			net_value += indent.net_value()
			remaining_quantity += indent.get_remaining_quantity()
			total_quantity += indent.quantity
		
		row['po_date'] = obj.get_date()
		row['net_value'] = f'{round(net_value,2)}'
		row["remaining_quantity"] = f'{int(remaining_quantity)} out of {int(total_quantity)}'
		row['Print'] = f'''<td class="">
				<a href="../report_input/{obj.pk}" >
				<img src="../../../static/Images/print.png" style="width:19px;height:19px" alt="print"></a>
			</td>'''
		row['Edit'] = f'''<td class="">
				<a href="../form/{obj.pk}" >
				<img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
			</td>'''
		row['Indent List'] = f'''<td class="">
				<a href="indent/table/{obj.pk}" >
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
		}
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
		indent_list_html = '<table class="table-bordered" style="width:100%">'
		indent_list_html += f'<tr><th class="d-flex justify-content-center">Indent</td><td class="">Balance</td></tr>'
		for indent in obj.indent_set.all():
			dimentions = f"{indent.size} X {indent.thickness} X {indent.width} X {indent.internal_diameter}".replace(" X None","").replace("None","")
			indent_list_html += f'<tr><td class="d-flex justify-content-left">{indent.pk} --&nbsp<a href="/wo/{indent.WO.pk}/indent/table" >{indent.WO}</a>&nbsp[{indent.item_description} ({dimentions})]</td><td class="">&nbsp&nbsp{indent.get_remaining_quantity()} out of {int(indent.quantity)}</td></tr>'
		indent_list_html += '</table>'

		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:80%">'
		for key in fields:
		    html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		
		html += '<tr><td class="">Indent List</td><td class="m-0 p-0">%s</td></tr>' % (indent_list_html)
		html += '</table>'
		return html

def update_indent_PO(indent_list,PO):
	'adds the PO to all the indents'
	my_indents = PO.indent_set.all()
	new_indents = set(indent.objects.all().filter(pk__in = indent_list))
	old_indents = set(my_indents)
	to_be_deleted = old_indents.difference(new_indents)
	to_be_saved = new_indents.difference(old_indents)
	for i in to_be_deleted:
		i.PO = None
		i.save()
	for i in to_be_saved:
		i.PO = PO
		i.save()

class PO_form(View):
	template_name = "po/PO_form.html"
	def get(self, request,po_id=None):
		self.context= {
			"update":[],
			'all_vendors':vendor_details.objects.all(),
			'all_indent':list(indent.objects.all().filter(PO=None).order_by("WO")),
		}
		if po_id:
			instance = purchase_order.objects.get(pk=po_id)
			my_indents = instance.indent_set.all()
			self.context['update'] = instance
			self.context['indent_list'] = my_indents
			self.context['all_indent'] += list(my_indents)
			self.context['success'] = False

		return render(request,self.template_name,self.context)

	def post(self, request,po_id=None):
		self.context= {
			"update":[],
			'all_vendors':vendor_details.objects.all(),
			'all_indent':list(indent.objects.all().filter(PO=None).order_by("WO")),
		}
		if po_id:
			instance = purchase_order.objects.get(pk=po_id)
			form = update_PO(request.POST,instance=instance)
		else:
			form = add_PO(request.POST)
		if form.is_valid():
			a = form.save()
			print(a)
			indent_list = request.POST.getlist('indent_list')
			update_indent_PO(indent_list,a)
			my_indents = a.indent_set.all()
			self.context['update'] = form.instance
			self.context['indent_list'] = my_indents
			self.context['all_indent'] += list(my_indents)
			self.context['all_indent'] = set(self.context['all_indent'])
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
			'all_PO': purchase_order.objects.all()
		}
		return render(request,self.template_name,context)
	def post(self, request):
		pass

def po_print_inputs(request,po_id):
	my_po = purchase_order.objects.get(pk=po_id)
	context = {'my_po':my_po}
	return render(request,"po/po_print_input.html",context)

def print_report(request,po_id):
	my_po = purchase_order.objects.get(pk=po_id)
	total_net_value = 0
	my_indents = indent.objects.all().filter(PO=my_po)
	total_gross_value,total_net_value,total_quantity,total_tax_value,total_weight = 0,0,0,0,0
	for my_indent in my_indents:
		total_net_value += my_indent.net_value()
		total_quantity += my_indent.quantity
		total_tax_value += my_indent.tax_amount()
		total_weight += my_indent.get_weight()
		total_gross_value += my_indent.gross_value()
	delivery_day = request.GET['delivery_day']
	payment_term = request.GET['payment_term']
	freight_charges = request.GET['freight_charges']
	print(freight_charges)
	context = {
		"my_po":my_po,
		"all_indents":my_indents,
		"total_net_value":round(total_net_value,2),
		"total_quantity":round(total_quantity,2),
		"total_tax_value":round(total_tax_value,2),
		"total_weight":round(total_weight,3),
		"total_gross_value":round(total_gross_value,2),
		"delivery_day":delivery_day,
		"payment_term":payment_term,
		"freight_charges":freight_charges,
	}
	print(context['total_net_value'])
	# total_quantity = indent.objects.all()
	return render(request,"po/report.html",context)

#endregion

#region ########### Work-Order ###########

def show_stock(request):
	stock_wo = work_order.objects.all().get(wo_number="STOCK")
	return redirect(f"/wo/{stock_wo.pk}/indent/table/")

class WO_datatable(AjaxDatatableView):
	model = work_order
	title = 'work_order'
	length_menu = [[25, 50, 100, -1], [25, 50, 100, 'all']]
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
		}, # wo_number
		{
			'name': 'description', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Description',
		}, # description
		{
			'name': 'quantity', 
			'visible': True,
			'orderable': True,
			'searchable': False,		
			'title': 'Quantity',
		}, # quantity
		{
			'name': 'net_value', 
			'visible': True,
			'orderable': False,
			'searchable': False,		
			'title': 'Net Value',
			'className': 'currency',
		}, # net_value
		{
			'name': 'is_complete', 
			'visible': True,
			'orderable': True,	
			'searchable': False,		
			'title': 'Completed',
		}, # is_complete
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

		queryset = self.model.objects.all().exclude(wo_number="STOCK")
		# queryset = queryset.filter(PO__id=po_id)
		# queryset = self.model.objects.all()
		return queryset
	
	def customize_row(self, row, obj):
		# 'row' is a dictionary representing the current row, and 'obj' is the current object.
		
		row['net_value'] = f''' {obj.net_value()}'''

		row['Edit'] = f'''<td class="">
				<a href="../form/{obj.pk}" >
				<img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
			</td>'''
		row['Indent List'] = f'''<td class="">
				<a href="/wo/{obj.pk}/indent/table/" >
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
			'PO Date':obj.incoming_po_date.strftime("%d-%m-%Y") if obj.incoming_po_date else "-----",
			'Tax':str(obj.tax)+"%",
		}
		currency={
			'Value':obj.value,
			'Discount':obj.discount,
			'Other Expanses':obj.other_expanses,
		}
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:60%">'
		for key in fields:
		    html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		for key in currency:
		    html += '<tr><td class="">%s</td><td class="currency">%s</td></tr>' % (key, currency[key])	
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
	def get(self, request,wo_id=None, *args, **kwargs):
		self.context= {
			"update":[],
			'all_vendors':vendor_details.objects.all(),
			"all_item_description":item_description.objects.all(),
		}
		if wo_id:
			instance = work_order.objects.get(pk=wo_id)
			self.context['update'] = instance
			self.context['success'] = False
			return render(request,self.template_name,self.context)
		else:
			self.context['update'] = []
			return render(request,self.template_name,self.context)
	def post(self, request,wo_id=None, *args, **kwargs):
		self.context= {
			"update":[],
			'all_vendors':vendor_details.objects.all(),
			"all_item_description":item_description.objects.all(),
		}
		tempdict = self.request.POST.copy()
		tempdict['value'] = tempdict['value'].replace(',', '').replace("₹","")
		if wo_id:
			instance = work_order.objects.get(pk=wo_id)
			form = add_WO(tempdict,instance=instance)
		else:
			form = add_WO(tempdict)
		if form.is_valid():
			form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.instance.value)
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)
#endregion

#region ########### Vendor ###########

class vendor_datatable(AjaxDatatableView):
	model = vendor_details
	title = 'vendor'
	length_menu = [[25, 50, 100, -1], [25, 50, 100, 'all']]
	initial_order = [["vendor_name","asc"]]
	search_values_separator = " "
	column_defs = [
		AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{
			'name': 'vendor_name', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Name',
		}, # name
		{
			'name': 'contact_person', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Contact Person',
		}, # contact_person
		{
			'name': 'email', 
			'visible': True,
			'orderable': True,
			'searchable': True,		
			'title': 'Email',
		}, # email
		{
			'name': 'contact_number', 
			'visible': True,
			'orderable': False,
			'searchable': False,		
			'title': 'Contact Number',
		}, # contact_number
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
		replace_empty = lambda x: x if x else "--"
		row['contact_person'] = replace_empty(row['contact_person'])
		row['contact_number'] = replace_empty(row['contact_number'])
		row['email'] = replace_empty(row['email'])

		row['Edit'] = f'''<td class="">
				<a href="../form/{obj.pk}" >
				<img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
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
			'Address':obj.address,
			'GST No.':obj.gst_no,
			'Name of Bank':obj.name_of_bank,
			'Account Number':obj.acc_no,
			'IFSC Code':obj.ifsc_code,
			'Branch':obj.branch,
			"Comment":obj.comment,
		}
		fields = {k: v for k, v in fields.items() if v != None}
		fields = {k: v for k, v in fields.items() if v != ""}
		# print(student_details.Division_id.Semester_id)
		html = '<table class="table-bordered" style="width:60%">'
		for key in fields:
			html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		html += '</table>'
		return html

class vendor_table(View):
	template_name = "vendor/vendor_table.html"
	context  = {}
	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,self.context)

	def post(self, request, *args, **kwargs):
		pks = request.POST.getlist("pks[]")
		for i in pks:
			obj = vendor_details.objects.filter(pk=i)[0]
			# print(obj)
			obj.delete()
		return JsonResponse({"deleted":True})
	
class vendor_form(View):
	template_name = "vendor/vendor_form.html"
	context= {
		"update":[]
	}
	def get(self, request,vendor_id=None, *args, **kwargs):
		if vendor_id:
			instance = vendor_details.objects.get(pk=vendor_id)
			self.context['update'] = instance
			self.context['success'] = False
			return render(request,self.template_name,self.context)
		else:
			self.context['update'] = []
			return render(request,self.template_name,self.context)
	
	def post(self, request,vendor_id=None, *args, **kwargs):
		tempdict = self.request.POST
		# print(tempdict['value'])
		if vendor_id:
			instance = vendor_details.objects.get(pk=vendor_id)
			form = add_vendor(tempdict,instance=instance)
		else:
			form = add_vendor(tempdict)
		if form.is_valid():
			form.save()
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.instance.value)
			print(form.errors)
		# self.context['update'] = form.instance
		return render(request,self.template_name,self.context)

#endregion

#region ########### GRN ###########

class grn_datatable(AjaxDatatableView):
	model = grn
	title = 'grn'
	length_menu = [[25, 50, 100, -1], [25, 50, 100, 'all']]
	initial_order = [["grn_date","asc"]]
	search_values_separator = " "
	column_defs = [
		# AjaxDatatableView.render_row_tools_column_def(),
		{
			'name': 'id',
			'visible': False,
			'searchable': False,
		},
		{
			'name': 'Vendor',
			'foreign_field': 'vendor_id__vendor_name',
			'visible': True,
			'searchable': True,
			'placeholder':'Vendor'
		}, # vendor
		{
			'name': 'invoice_no', 
			'visible': True,
			'searchable': True,
			'orderable': True,
			'title': 'Invoice Number',
		}, # invoice
		{
			'name': "indent_id", 
			'visible': True,
			'orderable': True,
			'searchable': False,
			'title': 'Indent',
		}, # indent
		{
			'name': 'quantity', 
			'visible': True,
			'orderable': True,
			'searchable': False,		
			'title': 'Quantity',
		}, # email
		{
			'name': "grn_date", 
			'visible': True,
			'orderable': True,
			'searchable': False,
			'title': 'GRN Date',
		}, # grn_date
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
		row['indent_id'] = str(obj.indent_id) if obj.indent_id else "---------"
		row['grn_date'] = obj.grn_date.strftime("%d-%m-%Y") if obj.grn_date else "-----"
		row['Vendor'] = obj.vendor_id.vendor_name if obj.vendor_id else "-------"
		row['Edit'] = f'''<td class="">
				<a href="../form/{obj.pk}" >
				<img src="../../../static/Images/editing.png" style="width:19px;height:19px" alt="edit"></a>
			</td>'''
		row['Delete'] =f'''<div class="form-check" onclick="checkSelected()">
				<input class="form-check-input del_input" type="checkbox"
				name="del" value="{obj.pk}" input_name="{obj}">
			</div>'''
		return

	def render_row_details(self, pk, request=None):
		# obj = self.model.objects.get(pk=pk)
		# # fields = [f for f in self.model._meta.get_fields() if f.concrete]
		# fields = {
		# 	'Address':obj.address,
		# 	'GST No.':obj.gst_no,
		# 	'Name of Bank':obj.name_of_bank,
		# 	'Account Number':obj.acc_no,
		# 	'IFSC Code':obj.ifsc_code,
		# 	'Branch':obj.branch,
		# 	"Comment":obj.comment,
		# }
		# fields = {k: v for k, v in fields.items() if v != None}
		# fields = {k: v for k, v in fields.items() if v != ""}
		# # print(student_details.Division_id.Semester_id)
		# html = '<table class="table-bordered" style="width:60%">'
		# for key in fields:
		# 	html += '<tr><td class="">%s</td><td class="">%s</td></tr>' % (key, fields[key])
		# html += '</table>'
		html = ""
		return html

class grn_table(View):
	template_name = "grn/grn_table.html"
	context  = {}
	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,self.context)

	def post(self, request, *args, **kwargs):
		pks = request.POST.getlist("pks[]")
		for i in pks:
			obj = grn.objects.filter(pk=i)[0]
			# print(obj)
			obj.delete()
		return JsonResponse({"deleted":True})
	
class grn_form(View):
	template_name = "grn/grn_form.html"

	def get(self, request,indent_id=None,grn_id=None, *args, **kwargs):
		self.context= {
			"update":[],
			"all_vendors":vendor_details.objects.all(),
		}
		if grn_id:
			instance = grn.objects.get(pk=grn_id)
			self.context["all_indent"]=indent.objects.all().filter(Q(recived=False)|Q(id=instance.indent_id.id))
			self.context['update'] = instance
			self.context['success'] = False
			return render(request,self.template_name,self.context)
		else:
			self.context['update'] = []
			self.context["all_indent"]=indent.objects.all().filter(Q(recived=False))
			if indent_id:
				my_indent = indent.objects.filter(id=indent_id).first()
				self.context['update'] = {"indent_id":my_indent}
				self.context["all_indent"]=indent.objects.all().filter(Q(recived=False)|Q(id=my_indent.id))
			return render(request,self.template_name,self.context)
	
	def post(self, request,grn_id=None, *args, **kwargs):
		self.context= {
			"update":[],
			"all_indent":indent.objects.all().filter(recived=False)
		}
		tempdict = self.request.POST.copy()
		tempdict['value'] = tempdict['value'].replace(',', '').replace("₹","")
		if grn_id:
			instance = grn.objects.get(pk=grn_id)
			form = add_grn(tempdict,instance=instance)
		else:
			form = add_grn(tempdict)
		if form.is_valid():
			self.context['save_message'] = form.instance.get_save_messages(tempdict['quantity'])
			form.save()
			print(tempdict['quantity'])
			self.context['update'] = form.instance
			self.context['success'] = True
		else:
			self.context['errors'] =  form.errors.as_ul()
			print(form.instance.value)
			print(form.errors)
		# return redirect("/grn/table")
		return render(request,self.template_name,self.context)

#endregion
