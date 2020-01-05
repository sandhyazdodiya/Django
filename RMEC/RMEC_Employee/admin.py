from django.contrib import admin
from .models import RMEC_Employee,User
from django.http import HttpResponse
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
import csv
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from django.db.models import Q
from django.urls import path
from import_export.admin import ImportExportModelAdmin

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'    
    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)    
    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice
class CertificateFilter(InputFilter):
        parameter_name = 'certificate'
        title = 'certificate'   
        def queryset(self, request, queryset):
            term = self.value()       
            if term is None:
                return       
            any_name = Q()
            for bit in term.split():
                any_name |= (
                    Q(certificate__icontains=bit) 
                )       
            return queryset.filter(any_name)
class EducationFilter(InputFilter):
        parameter_name = 'education'
        title = 'education'   
        def queryset(self, request, queryset):
            term = self.value()       
            if term is None:
                return       
            any_name = Q()
            for bit in term.split():
                any_name |= (
                    Q(education__icontains=bit) 
                )       
            return queryset.filter(any_name)
class WorkAreaFilter(InputFilter):
        parameter_name = 'work_area'
        title = 'work_area'   
        def queryset(self, request, queryset):
            term = self.value()       
            if term is None:
                return       
            any_name = Q()
            for bit in term.split():
                any_name |= (
                    Q(work_area__icontains=bit) 
                )       
            return queryset.filter(any_name)



class RMEC_EmployeeAdmin(ImportExportModelAdmin):
    admin.site.site_header = "RMEC Admin"
    admin.site.site_title = "RMEC Admin Portal"
    view_on_site = False
    admin.site.index_title = "Welcome to RMEC Admin Portal"
    list_display=('last_name','first_name','doc_no','correctional_facility','home_address','city','state','zip_code','phone','email','education','certificate','work_area','job_status','hired_date','created_date','updated_date')
    search_fields=('last_name','first_name','doc_no','correctional_facility','home_address','city','state','zip_code','phone','email','education','certificate','work_area','job_status','hired_date','created_date','updated_date')
   
    change_list_template = "admin/change_list.html"
    list_filter = (
        ('hired_date', DateRangeFilter),CertificateFilter,EducationFilter,WorkAreaFilter
    )
# class UserAdmin(admin.ModelAdmin):
#     list_display=('last_name',)
admin.site.register(User)
admin.site.register(RMEC_Employee,RMEC_EmployeeAdmin)



