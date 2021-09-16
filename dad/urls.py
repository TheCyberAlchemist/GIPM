"""dad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from main.views import *
urlpatterns = [
    # re_path('',WO_table.as_view(),name="show_wo_home"),    
    path('',home_page,name="home_page"),
    re_path(r'^wo/table/$',WO_table.as_view(),name="show_wo"),
    re_path(r'^wo/datatable/$',WO_datatable.as_view(),name="show_wo_datatable"),
    re_path(r'^wo/form/$',WO_form.as_view(),name="add_wo"),
    re_path(r'^wo/form/(?P<wo_id>\d+)/$',WO_form.as_view(),name="update_wo"),

    path('admin/', admin.site.urls),
    re_path(r'^wo/(?P<wo_id>\d+)/indent/table/',indent_table_page.as_view(),name="show_indent"),
    re_path(r'^wo/(?P<wo_id>\d+)/indent/datatable/',indent_table.as_view(),name="get_indent_details"),
    re_path(r'^wo/(?P<wo_id>\d+)/indent/form/$',indent_form.as_view(),name="add_indent"),
    re_path(r'^wo/(?P<wo_id>\d+)/indent/form/(?P<indent_id>\d+)/$',indent_form.as_view(),name="update_indent_form"),
    re_path(r'^wo/stock/$',show_stock,name="show_stock"),
    

    re_path(r'^po/table/$',PO_table.as_view(),name="show_po"),
    re_path(r'^po/datatable/$',PO_datatable.as_view(),name="show_po_datatable"),
    re_path(r'^po/form/$',PO_form.as_view(),name="add_po"),
    re_path(r'^po/form/(?P<po_id>\d+)/$',PO_form.as_view(),name="update_po"),
    re_path(r'^po/report_input/(?P<po_id>\d+)/$',po_print_inputs,name="po_report_input"),
    re_path(r'^po/report/(?P<po_id>\d+)/$',print_report,name="print_po_report"),

    re_path(r'^vendor/table/$',vendor_table.as_view(),name="show_vendor"),
    re_path(r'^vendor/datatable/$',vendor_datatable.as_view(),name="show_vendor_datatable"),
    re_path(r'^vendor/form/$',vendor_form.as_view(),name="add_vendor"),
    re_path(r'^vendor/form/(?P<vendor_id>\d+)/$',vendor_form.as_view(),name="update_vendor"),

    re_path(r'^grn/table/$',grn_table.as_view(),name="show_grn"),
    re_path(r'^grn/datatable/$',grn_datatable.as_view(),name="show_grn_datatable"),
    re_path(r'^indent/(?P<indent_id>\d+)/grn/form/$',grn_form.as_view(),name="add_indent_grn"),
    re_path(r'^grn/form/$',grn_form.as_view(),name="add_grn"),
    re_path(r'^grn/form/(?P<grn_id>\d+)/$',grn_form.as_view(),name="update_grn"),

]
