from django.test import TestCase
import pytest

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from django.test.client import RequestFactory

import json
from client.models import Company, Department, Employee, EmpProfile
from mixer.backend.django import mixer
from client.views import CompanyList, DepartmentList, EmployeeList, EmpProfileList


class TestCompanyView(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_company_list_url(self):
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_company_list_display_all(self):
        mixer.blend('client.Company', company_name="cybage")
        path = reverse('company_list')
        request = RequestFactory().get(path)

        response = CompanyList.as_view(actions={
            'get': 'list',
        })(request)
        assert response.status_code == 200
        assert list(response.data[0].items())[1][1] == "cybage"
    
    @pytest.mark.django_db
    def test_company_add(self):
        path = reverse('company_list')
        data = {'company_name': 'cybage'}
        request = RequestFactory().post(path, data, content_type='application/json')
        response = CompanyList.as_view(actions={
            'post': 'create',
        })(request)
        assert response.status_code == 201
        assert response.data['company_name'] == 'cybage'
    
    @pytest.mark.django_db
    def test_department_detail(self):
        mixer.blend('client.Company', company_name="cybage")
        path = reverse('dept_detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        response = CompanyList.as_view(actions={
            'get': 'retrieve',
        })(request, pk=1)
        assert response.status_code == 200
        assert response.data['company_name'] == 'cybage'

    @pytest.mark.django_db
    def test_company_detail_delete(self):
        mixer.blend('client.Company')
        path = reverse('company_detail', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        response = CompanyList.as_view(actions={
            'delete': 'destroy',
        })(request, pk=1)
        assert response.status_code == 204

class TestDepartmentView(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_department_list(self):
        response = self.client.get(reverse('dept_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @pytest.mark.django_db
    def test_department_list_all(self):
        mixer.blend('client.Department', dept_name=["HR department", "IS department"])
        path = reverse('dept_list')
        request = RequestFactory().get(path)

        response = DepartmentList.as_view(actions={'get': 'list'})(request)
        assert response.status_code == 200
        assert list(response.data[0].items())[1][1] == "['HR department', 'IS department']"

    @pytest.mark.django_db
    def test_department_add(self):
        path = reverse('dept_list')
        comp = Company.objects.create(company_name='cybage')
        data = {'dept_name': "['HR department', 'IS department']",'in_company': 'cybage'}
        request = RequestFactory().post(path, data, content_type='application/json')
        response = DepartmentList.as_view(actions={'post': 'create'})(request)
        assert response.status_code == 201
        assert response.data['dept_name'] == "['HR department', 'IS department']"

    @pytest.mark.django_db
    def test_department_detail(self):
        mixer.blend('client.Department', dept_name="IS department")
        path = reverse('dept_detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        response = DepartmentList.as_view(actions={
            'get': 'retrieve',
        })(request, pk=1)
        assert response.status_code == 200
        assert response.data['dept_name'] == 'IS department'
    
    @pytest.mark.django_db
    def test_department_detail_delete(self):
        mixer.blend('client.Department')
        path = reverse('dept_detail', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        response = DepartmentList.as_view(actions={
            'delete': 'destroy',
        })(request, pk=1)
        assert response.status_code == 204

class TestEmployeeView(TestCase):

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

    @pytest.mark.django_db
    def test_show_employee_detail(self):
        comp = Company.objects.create(company_name='cybage')
        dept = Department.objects.create(dept_name='HR department', in_company=comp)
        deptnew = Department.objects.create(dept_name='IS department', in_company=comp)
        mixer.blend('client.Employee', first_name="abhishek", last_name="bhujbal", role="MGR", address="nerul", phone=1234567890, in_dept=[1,2])
        path = reverse('emp_detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        response = EmployeeList.as_view(actions={
            'get': 'retrieve',
        })(request, pk=1)
        assert response.status_code == 200
        assert response.data['first_name'] == 'abhishek'
        assert response.data['last_name'] == 'bhujbal'
        assert response.data['role'] == 'MGR'
        assert response.data['address'] == 'nerul'
        assert response.data['in_dept'] == ['HR department', 'IS department']
    
    @pytest.mark.django_db
    def test_employee_delete(self):
        mixer.blend('client.Employee')
        path = reverse('emp_detail', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        response = EmployeeList.as_view(actions={
            'delete': 'destroy',
        })(request, pk=1)
        assert response.status_code == 204

class TestEmpProfileView(TestCase):

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
    
    @pytest.mark.django_db
    def test_empprofile_delete(self):
        mixer.blend('client.EmpProfile')
        path = reverse('empprof_detail', kwargs={'pk': 1})
        request = RequestFactory().delete(path)
        response = EmpProfileList.as_view(actions={
            'delete': 'destroy',
        })(request, pk=1)
        assert response.status_code == 204
    

