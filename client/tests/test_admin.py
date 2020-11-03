from django.test import TestCase
import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from client.models import Company, Department, Employee, EmpProfile

from django.contrib.admin.sites import AdminSite
from nested_admin import NestedStackedInline, NestedModelAdmin
from client.admin import CompanyAdmin, DepartmentAdmin, EmployeeAdmin
from django.urls import reverse
from rest_framework import status
from copy import deepcopy

class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin@#', email='admin@example.com')
        self.user.save()

    #check whether user type correct username and password
    def test_correct(self):
        user = authenticate(username='admin', password='admin@#')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_not_loggedin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/admin/')

    def test_loggedin(self):
        login = self.client.login(username='admin', password='admin@#')
        response = self.client.get(reverse('admin:index'))
        
    # checking user is logged in
        self.assertEqual(str(response.context['user']), 'admin')
    # checking "success"
        self.assertEqual(response.status_code, 200)   

    # checking username is false
    def test_wrong_username(self):
        user = authenticate(username='test', password='admin@#')
        self.assertFalse(user is not None and user.is_authenticated)

    # checking password is false
    def test_wrong_pssword(self):
        user = authenticate(username='admin', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class AdminViewTest(TestCase):
    
    def test_admin_header(self):
        self.assertEqual(admin.site.site_header, "CYBAGE MIS")
    
    def test_companyhascharfield(self):

        self.comp = Company.objects.create(company_name = 'cybage')

        self.assertEqual(self.comp.company_name,'cybage')
        self.assertNotEqual(self.comp.company_name,123)

    def test_depthascharfield(self):
        self.comp = Company.objects.create(company_name = 'cybage')
        self.dept = Department.objects.create(dept_name = 'HR dept',in_company=self.comp)

        self.assertEqual(self.dept.dept_name,'HR dept')
        self.assertNotEqual(self.dept.dept_name,123)

    def test_employeephoneunique(self):
        self.comp = Company.objects.create(company_name = 'cybage')
        self.dept = Department.objects.create(dept_name = 'HR dept',in_company=self.comp)


        desig = (
            ('BASE', 'base employee'),
            ('MGR', 'manager')
        )

        self.emp1 = Employee.objects.create(
            role = desig,
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567890
        )

        self.emp2 = Employee.objects.create(
            role = desig,
            first_name = "demo",
            last_name = "test",
            address = "Nerul",
            phone = 1234567891
        )

        self.assertNotEqual(self.emp1.phone, self.emp2.phone)


    def test_imagefieldofempprof(self):
        desig = (
            ('BASE', 'base employee'),
            ('MGR', 'manager')
        )

        self.emp = Employee.objects.create(
            role = desig,
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567890
        )
        
        self.emp_profile = EmpProfile.objects.create(
            emp = self.emp,
            image = '/media/abc.jpg'
            )

        self.assertEqual(EmpProfile.objects.count(), 1)
    

def _create_super_user():
    username = 'admin'
    password = User.objects.make_random_password()

    user = User.objects.create_superuser(
        email='admin@admin.com',
        password=password,
        username=username,
    )

    return (username, password)

class AdminCompanyTestCase(TestCase):
    # Payload obtained from Network -> Headers -> Form Data in Chrome
    company_form_post_payload = {
        "company_name": "cybage",

        "dept-TOTAL_FORMS": 1,
        "dept-INITIAL_FORMS": 0,
        "dept-MIN_NUM_FORMS": 0,
        "dept-MAX_NUM_FORMS": 1000,

        "dept-0-dept_name": 'HR',
        "dept-0-id": '',
        "dept-0-in_company":'' ,
        "dept-0-Employee_in_dept-TOTAL_FORMS": 0,
        "dept-0-Employee_in_dept-INITIAL_FORMS": 0,
        "dept-0-Employee_in_dept-MIN_NUM_FORMS": 0,
        "dept-0-Employee_in_dept-MAX_NUM_FORMS": 1000,
    }

    def setUp(self):
        (self.username, self.password) = _create_super_user()

        comp = Company.objects.create(company_name='demo')
        self.comp_id = comp.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/admin/')

    def test_response_if_logged_in(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('admin:index'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'admin')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)


    def test_comp_detail_form(self):
        self.client.login(
            username =self.username,
            password = self.password
        )

        response = self.client.get(
            reverse(
                'admin:client_company_change',
                args=(self.comp_id,),
            )
        )
        company = Company.objects.get(id=self.comp_id)

        self.assertContains(response, company.company_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_form_add(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:client_company_add'),
            self.company_form_post_payload,
        )

        company = Company.objects.get(company_name=self.company_form_post_payload["company_name"])
        dept = Department.objects.get(in_company = company.id)

        self.assertEqual(company.company_name, self.company_form_post_payload["company_name"])
        self.assertEqual(dept.dept_name, self.company_form_post_payload["dept-0-dept_name"])
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_company_form_change(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        # any changes made to a copy of object do not reflect in the original object
        company_form_post_payload = deepcopy(self.company_form_post_payload)
        company_form_post_payload['company_name'] = 'New Company'
        company_form_post_payload['dept-0-dept_name'] = 'HR updated'

        response = self.client.post(
            reverse(
                'admin:client_company_change',
                args=(self.comp_id,),
            ),
            company_form_post_payload
        )
        company = Company.objects.get(id=self.comp_id)
        dept = Department.objects.get(in_company=company.id)

        self.assertEqual(company.company_name, 'New Company')
        self.assertEqual(dept.dept_name, 'HR updated')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_delete_company(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse(
                'admin:client_company_delete',
                args=(self.comp_id,),
            ),
            {"post": "yes"}  # Are you sure? button
        )

        del_comp = Company.objects.filter(pk=self.comp_id).first()
        self.assertEqual(del_comp, None)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

class AdminEmployeeviewTest(TestCase):

    emp_form_post_payload = {
        "role": 'MGR',
        "first_name": "abhi",
        "last_name": "bhujbal",
        "address": "nerul",
        "phone": 2569784102,
        "empprofile-TOTAL_FORMS": 1,
        "empprofile-INITIAL_FORMS": 0,
        "empprofile-MIN_NUM_FORMS": 0,
        "empprofile-MAX_NUM_FORMS": 1,
    }
    emp_form_post_invalid_payload = deepcopy(emp_form_post_payload)

    def setUp(self):

        (self.username, self.password) = _create_super_user()

        comp = Company.objects.create(company_name='Test Company 1')
        dept1 = Department.objects.create(dept_name='Engineering', in_company=comp)

        self.emp = Employee.objects.create(
            role = 'MGR',
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567895, 
        )

        self.emp.in_dept.add(dept1)
        self.emp_form_post_payload['in_dept'] = dept1.pk

    def test_emp_detail_form(self):
        self.client.login(
            username = self.username,
            password = self.password
        )

        response = self.client.get(
            reverse(
                'admin:client_employee_change',
                args=(self.emp.id,),
            )
        )
        em = Employee.objects.get(id=self.emp.id)

        self.assertContains(response, em.first_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_emp_form_add(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )
        response = self.client.post(
            reverse('admin:client_employee_add'),
            self.emp_form_post_payload,
        )

        employee = Employee.objects.get(first_name=self.emp_form_post_payload["first_name"])

        self.assertEqual(employee.first_name, self.emp_form_post_payload["first_name"])
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_emp_add_invalid_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:client_employee_add'),
            self.emp_form_post_invalid_payload,
        )

        self.assertContains(response, 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_emp_change_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        # any changes made to a copy of object do not reflect in the original object
        emp_form_post_payload = deepcopy(self.emp_form_post_payload)
        emp_form_post_payload['role'] = 'BASE'

        response = self.client.post(
            reverse(
                'admin:client_employee_change',
                args=(self.emp.id,),
            ),
            emp_form_post_payload
        )
        employee = Employee.objects.get(id=self.emp.id)

        self.assertEqual(employee.role, 'BASE')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_emp_delete(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse(
                'admin:client_employee_delete',
                args=(self.emp.id,),
            ),
            {"post": "yes"}  # Are you sure? button
        )

        deleted = Employee.objects.filter(pk=self.emp.id).first()
        self.assertEqual(deleted, None)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)





