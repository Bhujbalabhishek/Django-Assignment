from django.urls import path, include
from . import views
from client.views import CompanyList, DepartmentList, EmployeeList, EmpProfileList
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# from rest_framework_extensions.routers import NestedRouterMixin

router = DefaultRouter()

router.register(r'companys', CompanyList)

dept_router = routers.NestedSimpleRouter(router, r'companys', lookup = 'company')
dept_router.register(r'departments', DepartmentList, basename = 'departments')

emp_router = routers.NestedSimpleRouter(dept_router, r'departments', lookup = 'department')
emp_router.register(r'employees', EmployeeList, basename = 'employees')

# router.register(r'department', DepartmentList)
# router.register(r'employee', EmployeeList)
router.register(r'empprof', EmpProfileList)

urlpatterns =[
    path('', include(router.urls)),
    path('',include(dept_router.urls)),
    path('',include(emp_router.urls)),
]

# router = DefaultRouter()

# router.register(r'companys', CompanyList)
# router.register(r'department', DepartmentList)
# router.register(r'employee', EmployeeList)
# router.register(r'empprof', EmpProfileList)

# class NestedDefaultRouter(NestedRouterMixin,DefaultRouter):
#     pass

# router = NestedDefaultRouter()

# comp_router= router.register(r'companys', CompanyList)

# comp_router.register(
#     'department',
#     DepartmentList,
#     basename = 'departments',
#     parent_query_lookups = ['company']
# )






















### Using the url patterns with api root funcion that I defined in views.py ###

# comp_list = CompanyList.as_view({
#     'get' : 'list'
# })

# comp_detail = CompanyList.as_view({
#     'get' : 'retrieve'
# })

# dept_list = DepartmentList.as_view({
#     'get' : 'list',
#     'post' : 'create'
# })

# dept_detail = DepartmentList.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy'
# })

# employee_list = EmployeeList.as_view({
#     'get' : 'list',
#     'post' : 'create'
# })

# employee_detail = EmployeeList.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy'
# })

# empprof_list = EmpProfileList.as_view({
#     'get' : 'list'
# })

# empprof_detail = EmpProfileList.as_view({
#     'get' : 'retrieve',
#     'delete' : 'destroy'
# })

# urlpatterns = [
#     path('', api_root),
#     path('company/',comp_list, name = "company_list"),
#     path('company/<int:pk>/',comp_detail, name = "company_detail"),
#     path('department/',dept_list, name = "dept_list"),
#     path('department/<int:pk>/',dept_detail, name = "dept_detail"),
#     path('employee/',employee_list, name = "emp_list"),
#     path('employee/<int:pk>/',employee_detail, name = "emp_detail"),
#     path('empprof/',empprof_list, name = "empprof_list"),
#     path('empprof/<int:pk>/',empprof_detail, name = "empprof_detail"),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)