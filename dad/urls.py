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
    path('admin/', admin.site.urls),
    re_path(r'indent/table/(?P<po_id>\d+)/',indent_table_page.as_view(),name="show_indent_table"),
    re_path(r'indent/table/get_indent_details/',indent_table.as_view(),name="get_indent_details"),
    re_path(r'^indent/form/$',indent_form.as_view(),name="show_indent_form"),
    re_path(r'^indent/form/(?P<indent_id>\d+)/$',indent_form.as_view(),name="update_indent_form"),
    
    re_path(r'^po/table/$',PO_table.as_view(),name="show_po"),
    re_path(r'^po/form/(?P<po_id>\d+)/$',PO_table.as_view(),name="update_po"),


]
