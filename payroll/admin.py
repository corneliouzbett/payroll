from django.contrib import admin
from models import *

class DepartmentAdmin(admin.ModelAdmin):
    list_displays=('name',)
    search_fields=('name',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display=('employeeId','name')
    search_fields=('id','name')

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_displays=('name',)
    search_fields=('name',)

admin.site.register(Department,DepartmentAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(EmployeeType,EmployeeTypeAdmin)
admin.site.register(AttendRecord)
admin.site.register(Notice)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Payroll)
