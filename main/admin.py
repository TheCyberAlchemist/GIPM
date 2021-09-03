from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(item_description)
# admin.site.register(work_order)
admin.site.register(purchase_order)
admin.site.register(standard_weight)
admin.site.register(indent)
admin.site.register(vendor_details)
@admin.register(work_order)
class WOAdmin(admin.ModelAdmin):
	list_display = ['wo_number','vendor_id']