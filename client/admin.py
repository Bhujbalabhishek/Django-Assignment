from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Company, Department, Employee, EmpProfile
from django_reverse_admin import ReverseModelAdmin
from nested_admin import NestedStackedInline, NestedModelAdmin

admin.site.site_header = "CYBAGE MIS"

#using Django-Nested-Admin
class DepartmentAdmin(NestedStackedInline):
    model = Department
    extra = 1
    

#using Django-Nested-Admin
class EmpProfileAdmin2(NestedStackedInline):
    model = EmpProfile

#using Django-Reverse-Admin
class EmpProfileAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [
                      ('emp', {'fields': ['role', 'first_name','last_name', 'phone','address','in_dept']}),
                     ]
    list_display = ('emp','image_tag')
    list_display_links = ('emp','image_tag')
    readonly_fields = ['image_tag']

#using Django-Nested-Admin
class EmployeeAdmin(NestedModelAdmin):
    model = Employee
    inlines = [EmpProfileAdmin2]
    list_display = ('first_name', 'last_name', 'phone', 'dept', 'role')
    list_display_links = ('first_name', 'phone', 'dept', 'role' )
    
    def dept(self,obj):
        return ','.join([in_dept.dept_name for in_dept in obj.in_dept.all()])

#using Django-Nested-Admin
class CompanyAdmin(NestedModelAdmin):
    model = Company
    inlines = [DepartmentAdmin]



admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmpProfile, EmpProfileAdmin)







## before used the basic ModelAdmin and StackedInline ##

# class DepartmentAdmin(admin.StackedInline):
#     model = Department
#     extra = 1

# class EmpProfileAdmin2(admin.StackedInline):
#     model = EmpProfile

# class EmployeeAdmin(admin.ModelAdmin):
#     model = Employee
#     inlines = [EmpProfileAdmin2]
#     list_display = ('first_name', 'last_name', 'phone', 'dept', 'role')
#     list_display_links = ('first_name', 'phone', 'dept', 'role' )
    
#     def dept(self,obj):
#         return ','.join([in_dept.dept_name for in_dept in obj.in_dept.all()])

# class CompanyAdmin(admin.ModelAdmin):
#     model = Company
#     inlines = [DepartmentAdmin]