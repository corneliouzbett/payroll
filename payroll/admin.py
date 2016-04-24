from django.contrib import admin
from models import *

class DepartmentAdmin(admin.ModelAdmin):
    list_displays=('department_id','department_name')
    search_fields=('department_name','department_id')

class EmployeeAdmin(admin.ModelAdmin):
    list_display=('id','name')
    search_fields=('id','name')

class Employee_typeAdmin(admin.ModelAdmin):
    list_displays=('employee_type_id','employee_type')
    search_fields=('employee_type','employee_type_id')

admin.site.register(Department,DepartmentAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Employee_type,Employee_typeAdmin)
