from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Company, Department, Employee, EmpProfile


admin.site.site_header = "CYBAGE MIS"

class DepartmentAdmin(admin.StackedInline):
    model = Department
    extra = 1

class EmpProfileAdmin(admin.StackedInline):
    model = EmpProfile

class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    inlines = [EmpProfileAdmin]
    list_display = ('first_name', 'last_name', 'phone', 'dept', 'role')
    list_display_links = ('first_name', 'phone', 'dept', 'role' )
    
    def dept(self,obj):
        return ','.join([in_dept.dept_name for in_dept in obj.in_dept.all()])

class CompanyAdmin(admin.ModelAdmin):
    model = Company
    inlines = [DepartmentAdmin]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmpProfile)