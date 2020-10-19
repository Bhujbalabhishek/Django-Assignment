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


class CompanyList(viewsets.ModelViewSet):

    
    serializer_class = Company_Serializer
    queryset = Company.objects.all()

    # def get(self, request):
    #     company1 = Company.objects.all()
    #     serializer = Company_Serializer(company1, many = True)
    #     return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter()
        return query_set

class DepartmentList(viewsets.ModelViewSet):

    
    serializer_class = Department_Serializer
    queryset = Department.objects.all()


    # def get_queryset(self):
    #     queryset = self.queryset
    #     query_set = queryset.filter(id = self.kwargs['id'])
    #     return query_set


class EmployeeList(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = Employee_Serializer

class EmpProfileList(viewsets.ModelViewSet):

    queryset = EmpProfile.objects.all()
    serializer_class = EmpProfile_Serializer

@api_view(['GET'])
def api_root(request,format = None):
    return Response({
        'company': reverse('company_list', request = request, format = format),
        'department': reverse('dept_list', request = request, format = format),
        'employee': reverse('emp_list', request = request, format = format),
        'empprofile': reverse('empprof_list', request = request, format = format)
    })