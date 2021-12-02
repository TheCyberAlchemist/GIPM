from django.contrib import admin
from .models import *
print(work_order.objects.get_or_create(wo_number="STOCK"))


@admin.register(standard_weight)
class SW(admin.ModelAdmin):
	list_display = ["material_shape","size",'weight_pmm']
	search_fields=('material_shape',)
	list_filter= ['material_shape']

@admin.register(grn)
class grn(admin.ModelAdmin):
	list_display = ["invoice_no","vendor_id",'indent_id']
	search_fields=('invoice_no',)


@admin.register(purchase_order)
class PO(admin.ModelAdmin):
	list_display = ["po_number","vendor_id",'po_date']
	search_fields=('po_number',"po_date","vendor_id__vendor_name")

@admin.register(vendor_details)
class vendor(admin.ModelAdmin):
	list_display = ["vendor_name",'contact_person',"gst_no"]
	search_fields=('vendor_name',"address","contact_person")

@admin.register(indent)
class indent(admin.ModelAdmin):
	list_display = ["id","WO",'material_shape',"item_description"]
	search_fields=("id",'WO__wo_number',"material_shape","item_description__description")
	list_filter= ['material_shape']

@admin.register(work_order)
class WOAdmin(admin.ModelAdmin):
	list_display = ['wo_number','vendor_id']
	search_fields=('wo_number',)

@admin.register(item_description)
class description(admin.ModelAdmin):
	list_display = ['description']
	search_fields=('description',)

@admin.register(assembly)
class assembly(admin.ModelAdmin):
	list_display = ["name","description","estimate_value"]
	search_fields=('name',)
	# list_filter= ['material_shape']
