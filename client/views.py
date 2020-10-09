from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Company, Department, Employee, EmpProfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from client.serializers import Company_Serializer, Department_Serializer, Employee_Serializer, EmpProfile_Serializer
from rest_framework import viewsets


class CompanyList(APIView):

    def get(self, request):
        company1 = Company.objects.all()
        serializer = Company_Serializer(company1, many = True)
        return Response(serializer.data)


class DepartmentList(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = Department_Serializer

    # def get(self, request):
    #     department1 = Department.objects.all()
    #     serializer = Department_Serializer(department1, many = True)
    #     return Response(serializer.data)


class EmployeeList(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = Employee_Serializer

    # def get(self, request):
    #     employee1 = Employee.objects.all()
    #     serializer = Employee_Serializer(employee1, many = True)
    #     return Response(serializer.data)


class EmpProfileList(viewsets.ModelViewSet):

    queryset = EmpProfile.objects.all()
    serializer_class = EmpProfile_Serializer

    # def get(self, request):
    #     empprof1 = EmpProfile.objects.all()
    #     serializer = EmpProfile_Serializer(empprof1, many = True)
    #     return Response(serializer.data)
    

@api_view(['GET'])
def api_root(request, format = None):
    return Response({
        'company': reverse('company_list', request = request, format = format),
        'department': reverse('dept_list', request = request, format = format),
        'employee': reverse('emp_list', request = request, format = format),
        'empprofile': reverse('empprof_list', request = request, format = format)
    })