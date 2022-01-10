from django.contrib import admin
from django.urls import path,re_path
from main.views import *
from main.api.views import *
from main.export_excel import *


urlpatterns = [
	# re_path('',WO_table.as_view(),name="show_wo_home"),
	path('admin/', admin.site.urls),
	path('',home_page,name="home_page"),
	#region ########### WO ########################
	re_path(r'^wo/table/$',WO_table.as_view(),name="show_wo"),
	re_path(r'^wo/datatable/$',WO_datatable.as_view(),name="show_wo_datatable"),
	re_path(r'^wo/form/$',WO_form.as_view(),name="add_wo"),
	re_path(r'^wo/form/(?P<wo_id>\d+)/$',WO_form.as_view(),name="update_wo"),
	# endregion
	#region ########### WO_indents ################
	re_path(r'^wo/(?P<wo_id>\d+)/indent/table/',indent_table_page.as_view(),name="show_indent"),
	re_path(r'^wo/(?P<wo_id>\d+)/indent/datatable/',indent_table.as_view(),name="get_indent_details"),
	re_path(r'^wo/(?P<wo_id>\d+)/indent/form/$',indent_form.as_view(),name="add_indent"),
	re_path(r'^wo/(?P<wo_id>\d+)/indent/form/(?P<indent_id>\d+)/$',indent_form.as_view(),name="update_indent_form"),
	re_path(r'^wo/stock/$',show_stock,name="show_stock"),
	path('all_indent/',all_indent_table.as_view(),name="show_all_indent"),
	re_path(r'^all_indent/datatable/',all_indents_datatable.as_view(),name="get_all_indent"),
	re_path(r'^wo/print_indents/(?P<wo_id>\d+)/$',print_wo_indents,name="print_wo_indents"),
	re_path(r'^wo/print_indents/(?P<wo_id>\d+)/excel',export_wo_xls,name="print_wo_excel"),
	# endregion
	#region ########### PO ########################
	re_path(r'^po/table/$',PO_table.as_view(),name="show_po"),
	re_path(r'^po/datatable/$',PO_datatable.as_view(),name="show_po_datatable"),
	re_path(r'^po/form/$',PO_form.as_view(),name="add_po"),
	re_path(r'^po/form/(?P<po_id>\d+)/$',PO_form.as_view(),name="update_po"),
	re_path(r'^po/report_input/(?P<po_id>\d+)/$',po_print_inputs,name="po_report_input"),
	re_path(r'^po/report/(?P<po_id>\d+)/$',print_report,name="print_po_report"),
	re_path(r'^po/report/(?P<po_id>\d+)/lock$',lock_po_indent,name="lock_po_indents"),
	re_path(r'^po/report/(?P<po_id>\d+)/excel',export_po_xls,name="print_po_excel"),
	# endregion
	#region ########### Vendor ####################
	re_path(r'^vendor/table/$',vendor_table.as_view(),name="show_vendor"),
	re_path(r'^vendor/datatable/$',vendor_datatable.as_view(),name="show_vendor_datatable"),
	re_path(r'^vendor/form/$',vendor_form.as_view(),name="add_vendor"),
	re_path(r'^vendor/form/(?P<vendor_id>\d+)/$',vendor_form.as_view(),name="update_vendor"),
	# endregion
	#region ########### GRN #######################
	re_path(r'^grn/table/$',grn_table.as_view(),name="show_grn"),
	re_path(r'^grn/datatable/$',grn_datatable.as_view(),name="show_grn_datatable"),
	re_path(r'^indent/(?P<indent_id>\d+)/grn/form/$',grn_form.as_view(),name="add_indent_grn"),
	re_path(r'^grn/form/$',grn_form.as_view(),name="add_grn"),
	re_path(r'^grn/form/(?P<grn_id>\d+)/$',grn_form.as_view(),name="update_grn"),
	# endregion
	#region ########### Assembly ##################
	re_path(r'^assembly/table/$',assembly_table.as_view(),name="show_assembly"),
	re_path(r'^assembly/datatable/$',assembly_datatable.as_view(),name="show_assembly_datatable"),
	re_path(r'^assembly/form/$',assembly_form.as_view(),name="add_assembly"),
	re_path(r'^assembly/form/(?P<assembly_id>\d+)/$',assembly_form.as_view(),name="update_assembly"),
	# API for assembly
	re_path(r'^api/assembly$',assemblyList.as_view(),name="api_assembly"),
	re_path(r'^api/assembly/(?P<pk>\d+)/$',assemblyRUD.as_view(),name="api_assembly"),
	re_path(r'^api/item-description$',ItemDescriptionList.as_view(),name="api_item_description"),
	re_path(r'^api/assembly/calculate-estimate$',calculate_assembly_estimate,name="calculate_assembly_estimate"),
	# endregion
	#region ########### Plan ######################
	re_path(r'^plan/form/$',plan_form.as_view(),name="add_plan"),
	re_path(r'^plan/form/(?P<plan_id>\d+)/$',plan_form.as_view(),name="update_plan"),
	re_path(r'^plan/table/$',plan_table.as_view(),name="show_plan"),
	re_path(r'^plan/datatable/$',plan_datatable.as_view(),name="show_plan_datatable"),
	
	# API for plan
	re_path(r'^api/plan$',planList.as_view(),name="api_plan"),
	re_path(r'^api/plan/(?P<pk>\d+)/$',planRUD.as_view(),name="api_plan"),
	re_path(r'^api/plan/calculate-estimate$',calculate_plan_estimate,name="calculate_plan_estimate"),
	re_path(r'^api/get_last_indent/$',get_last_indent_by_item,name="get_indent_json_by_item_description"),
	# endregion
]
