from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Company, Department, Employee, EmpProfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from client.serializers import Company_Serializer, Department_Serializer, Employee_Serializer, EmpProfile_Serializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics


class CompanyList(viewsets.ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = Company_Serializer
    
class DepartmentList(viewsets.ModelViewSet):

    serializer_class = Department_Serializer

    def get_queryset(self):
        return Department.objects.filter(in_company = self.kwargs['company_pk'])
    
class EmployeeList(viewsets.ModelViewSet):

    serializer_class = Employee_Serializer

    def get_queryset(self):
        return Employee.objects.filter(in_dept = self.kwargs['department_pk'])

class EmpProfileList(viewsets.ModelViewSet):

    queryset = EmpProfile.objects.all()
    serializer_class = EmpProfile_Serializer

























# @api_view(['GET'])
# def api_root(request,format = None):
#     return Response({
#         'company': reverse('company_list', request = request, format = format),
#         'department': reverse('dept_list', request = request, format = format),
#         'employee': reverse('emp_list', request = request, format = format),
#         'empprofile': reverse('empprof_list', request = request, format = format)
#     })