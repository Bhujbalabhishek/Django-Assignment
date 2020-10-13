from django.urls import path, include
from . import views
from client.views import CompanyList, DepartmentList, EmployeeList, EmpProfileList, api_root
from rest_framework.urlpatterns import format_suffix_patterns


dept_list = DepartmentList.as_view({
    'get' : 'list',
    'post' : 'create'
})

dept_detail = DepartmentList.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})

employee_list = EmployeeList.as_view({
    'get' : 'list',
    'post' : 'create'
})

employee_detail = EmployeeList.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})

empprof_list = EmpProfileList.as_view({
    'get' : 'list'
})

empprof_detail = EmpProfileList.as_view({
    'get' : 'retrieve',
    'delete' : 'destroy'
})

urlpatterns = [
    path('', api_root),
    path('company/',CompanyList.as_view(), name = "company_list"),
    path('department/',dept_list, name = "dept_list"),
    path('department/<int:pk>/',dept_detail, name = "dept_detail"),
    path('employee/',employee_list, name = "emp_list"),
    path('employee/<int:pk>/',employee_detail, name = "emp_detail"),
    path('empprof/',empprof_list, name = "empprof_list"),
    path('empprof/<int:pk>/',empprof_detail, name = "empprof_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)