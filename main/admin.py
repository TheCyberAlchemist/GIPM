from django.contrib import admin
from .models import *

admin.site.register(purchase_order)
admin.site.register(standard_weight)
admin.site.register(vendor_details)

@admin.register(indent)
class indent(admin.ModelAdmin):
	list_display = ["WO",'material_shape',"item_description"]
	search_fields=('WO__wo_number',"material_shape","item_description__description")
@admin.register(work_order)
class WOAdmin(admin.ModelAdmin):
	list_display = ['wo_number','vendor_id']
	search_fields=('wo_number',)

@admin.register(item_description)
class description(admin.ModelAdmin):
	list_display = ['description']
	search_fields=('description',)