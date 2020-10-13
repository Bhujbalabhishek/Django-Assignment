from django.test import TestCase
import unittest
import pytest

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

import json
from client.models import Company, Department, Employee, EmpProfile

class TestCompanyView(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_company_list(self):
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDepartmentView(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_department_list(self):
        response = self.client.get(reverse('dept_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @pytest.mark.django_db
    def test_department_post(self):
        url = '/department/'
        comp = Company.objects.create(company_name='cybage')
        dept = Department.objects.create(dept_name='HR department', in_company=comp)

        data = {'dept_name': 'HR department','in_company':'cybage' }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

  
    @pytest.mark.django_db
    def test_department_detail(self):
        obj = Department.objects.all()
        if obj:
            response = self.client.get(reverse('dept_detail', args=[obj[0].id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestEmployeeView(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_employee_list(self):
        response = self.client.get(reverse('emp_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @pytest.mark.django_db
    def test_employee_post(self):
        url = '/employee/'
        comp = Company.objects.create(company_name='cybage')
        dept = Department.objects.create(dept_name='HR department', in_company=comp)

        data = {'role': 'MGR','first_name':'abhishek','last_name':'bhujbal','address':'nerul', 'phone':1234567890, 'in_dept':['HR department'] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    @pytest.mark.django_db
    def test_employee_detail(self):
        obj = Employee.objects.all()
        if obj:
            response = self.client.get(reverse('emp_detail', args=[obj[0].id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestEmpProfileView(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_empprof_list(self):
        response = self.client.get(reverse('empprof_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_empprof_detail(self):
        obj = EmpProfile.objects.all()
        if obj:
            response = self.client.get(reverse('empprof_detail', args=[obj[0].id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)